# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""The utilities module with many helpful things used by other modules."""
from __future__ import annotations

import asyncio
import asyncio.subprocess
import logging
import os
import random
import re
import time
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Callable, Optional, Tuple, Type, TypeVar, Union

import tornado.httputil
from tornado.web import RequestHandler

from an_website import DIR as SITE_BASE_DIR

GIT_URL: str = "https://github.com/asozialesnetzwerk"
REPO_URL: str = f"{GIT_URL}/an-website"

Handler = Union[
    tuple[str, Type[RequestHandler]],
    tuple[str, Type[RequestHandler], dict[str, Any]],
    tuple[str, Type[RequestHandler], dict[str, Any], str],
]
# following should be tuple[Handler, ...] but mypy then complains
HandlerTuple = Tuple[Handler, ...]


# sortable so the pages can be linked in a order
# frozen so it's immutable
@dataclass(order=True, frozen=True)
class PageInfo:
    """The page info class that is used for the subpages of a module info."""

    name: str
    description: str
    path: Optional[str] = None
    # keywords, that can be used for searching
    keywords: tuple[str, ...] = field(default_factory=tuple)


@dataclass(order=True, frozen=True)
class ModuleInfo(PageInfo):
    """
    The module info class adds handlers and sub pages to the page info.

    This gets created by every module to add the handlers.
    """

    handlers: HandlerTuple = field(default_factory=HandlerTuple)
    sub_pages: tuple[PageInfo, ...] = field(default_factory=tuple)
    aliases: tuple[str, ...] = field(default_factory=tuple)

    def get_page_info(self, path: str) -> PageInfo:
        """Get the page_info of that specified path"""
        if self.path == path:
            return self

        for page_info in self.sub_pages:
            if page_info.path == path:
                return page_info

        return self

    def get_keywords_as_str(self, path: str) -> str:
        """Get the keywords as comma seperated string."""
        page_info = self.get_page_info(path)
        if self != page_info:
            return ", ".join((*self.keywords, *page_info.keywords))

        return ", ".join(self.keywords)


# def mkdir(path: str) -> bool:
#     """Create a dir and return whether it got created."""
#     try:
#         os.mkdir(path)
#         return True
#     except FileExistsError:
#         return False


class Timer:
    """Timer class used for timing stuff."""

    def __init__(self):
        """Start the timer."""
        self._execution_time: Optional[float] = None
        self._start_time: float = time.time()

    def stop(self) -> float:
        """
        Stop the timer and return the execution time in seconds.

        If the timer was stopped already a ValueError gets raised.
        """
        if self._execution_time is not None:
            raise ValueError("Timer has been stopped before.")
        self._execution_time = time.time() - self._start_time

        del self._start_time
        return self._execution_time

    @property
    def execution_time(self) -> float:
        """
        Get the execution time in seconds and return it.

        If the timer wasn't stopped yet a ValueError gets raised.
        """
        if self._execution_time is None:
            raise ValueError("Timer wasn't stopped yet.")
        return self._execution_time


T = TypeVar("T")  # pylint: disable=invalid-name


def time_function(function: Callable[..., T], *args: Any) -> tuple[T, float]:
    """Run the function and return the result and the time it took in s."""
    timer = Timer()
    return function(*args), timer.stop()


def length_of_match(_m: re.Match):
    """Calculate the length of the regex match and return it."""
    span = _m.span()
    return span[1] - span[0]


def n_from_set(_set: Union[set[T], frozenset[T]], _n: int) -> set[T]:
    """Get and return _n elements of the set as a new set."""
    i = 0
    new_set = set()
    for _el in _set:
        if i < _n:
            i += 1
            new_set.add(_el)
        else:
            break
    return new_set


def bool_to_str(val: bool) -> str:
    """Convert a boolean to sure/nope."""
    return "sure" if val else "nope"


def str_to_bool(val: str, default: Optional[bool] = None) -> bool:
    """Convert a string representation of truth to True or False."""
    val = val.lower()
    if val in ("sure", "y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("nope", "n", "no", "f", "false", "off", "0"):
        return False
    if val in ("maybe", "idc"):
        return random.choice((True, False))
    if default is None:
        raise ValueError(f"invalid truth value '{val}'")
    return default


async def run(
    programm, *args, stdin=asyncio.subprocess.PIPE
) -> tuple[Optional[int], bytes, bytes]:
    """Run a programm & return the return code, stdout and stderr as tuple."""
    proc = await asyncio.create_subprocess_exec(
        programm,
        *args,
        stdin=stdin,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    com = proc.communicate()
    # important:
    stdout, stderr = await com

    return proc.returncode, stdout, stderr


async def run_shell(
    cmd, stdin=asyncio.subprocess.PIPE
) -> tuple[Optional[int], bytes, bytes]:
    """Run the cmd and return the return code, stdout and stderr in a tuple."""
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdin=stdin,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    com = proc.communicate()

    # debugging stuff:
    if "ps -p" not in cmd:
        with open(f"/proc/{proc.pid}/stat", encoding="utf-8") as file:
            print(file.read())
        await (run(f"ps -p {proc.pid} all | grep -E 'PID|{proc.pid}'"))

    # important:
    stdout, stderr = await com

    # debugging stuff:
    if "ps -p" in cmd:
        logger = logging.getLogger(__name__)
        logger.error(
            str(
                {
                    "code": proc.returncode,
                    "stdout": stdout.decode("utf-8"),
                    "stderr": stderr.decode("utf-8"),
                }
            )
        )

    return proc.returncode, stdout, stderr


@cache
def add_args_to_url(url: str, **kwargs) -> str:
    """Add a query arguments to a url."""
    if len(kwargs) == 0:
        return url

    url_args: dict[str, str] = {}

    for key, value in kwargs.items():
        if value is not None:
            if isinstance(value, bool):
                url_args[key] = bool_to_str(value)
            else:
                url_args[key] = str(value)

    return tornado.httputil.url_concat(url, url_args)


def get_themes() -> tuple[str, ...]:
    """Get a list of available themes."""
    files = os.listdir(os.path.join(SITE_BASE_DIR, "static/style/themes"))

    return (
        *(file[:-4] for file in files if file.endswith(".css")),
        "random",  # add random to the list of themes
        "random-dark",
    )


THEMES: tuple[str, ...] = get_themes()
