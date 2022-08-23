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

"""Parse data into classes."""

from __future__ import annotations

import functools
import inspect
import typing
from collections.abc import Callable
from inspect import Parameter
from types import UnionType
from typing import Any, TypeVar, get_origin

from tornado.web import HTTPError, RequestHandler

from .utils import str_to_bool

T = TypeVar("T")


def parse(
    type_: type[T],
    data: list[dict[str, Any]] | dict[str, Any] | Any,
    *,
    strict: bool = False,
) -> T:
    """Parse a data."""
    # pylint: disable=too-many-return-statements
    simple_type: type = get_origin(type_) or type_
    if simple_type == UnionType:
        if isinstance(data, type_):
            return data
        possible = list(typing.get_args(type_))
        if len(possible) != 2 or None not in possible:
            raise ValueError("Cannot parse all Unions, only optionals.")
        possible.remove(None)
        type_ = possible[0]
        simple_type = get_origin(type_) or type_

    if simple_type in {list, "list"} and isinstance(data, list):
        return _parse_list(type_, data, strict=strict)
    if type_ in {bool, "bool"}:
        return typing.cast(T, _parse_bool(data, strict=strict))
    if type_ in {str, "str"}:
        return typing.cast(T, _parse_str(data, strict=strict))
    if type_ in {int, "int"}:
        return typing.cast(T, _parse_int(data, strict=strict))
    if type_ in {float, "float"}:
        return typing.cast(T, _parse_float(data, strict=strict))
    if hasattr(type_, "__init__") and isinstance(data, dict):
        return _parse_class(type_, data, strict=strict)

    raise ValueError(f"Unable to parse {data!r} into {type_}")


def _parse_str(data: Any, *, strict: bool) -> str:
    """Parse data into str."""
    if isinstance(data, str):
        return data
    if strict:
        raise ValueError(f"{data!r} is not str.")
    return str(data)


def _parse_bool(data: Any, *, strict: bool) -> bool:
    """Parse data into bool."""
    if isinstance(data, bool):
        return data
    if strict:
        raise ValueError(f"{data!r} is not bool.")
    if data in {0, 1}:
        return bool(data)
    if isinstance(data, str):
        return str_to_bool(data)
    raise ValueError(f"Cannot parse {data!r} into bool.")


def _parse_int(data: Any, *, strict: bool) -> int:
    """Parse data into int."""
    if isinstance(data, int):
        return data
    if isinstance(data, float) and int(data) == data:
        return int(data)
    if strict:
        raise ValueError(f"{data!r} is not a number.")
    if isinstance(data, str):
        return int(data, base=0)
    if isinstance(data, bool):
        return int(data)
    raise ValueError(f"Cannot parse {data!r} into int.")


def _parse_float(data: Any, *, strict: bool) -> float:
    """Parse data into float."""
    if isinstance(data, float):
        return data
    if isinstance(data, int):
        return float(data)
    if strict:
        raise ValueError(f"{data!r} is not a number.")
    if isinstance(data, str):
        return int(data)
    if isinstance(data, bool):
        return int(data)
    raise ValueError(f"Cannot parse {data!r} into int.")


def _parse_list(
    type_: type[T], data: list[dict[str, Any]], *, strict: bool
) -> T:
    """Parse a list of data."""
    args = typing.get_args(type_)
    if len(args) != 1:
        raise ValueError(f"{type_=} should be list[...]")
    return typing.cast(
        T, [parse(args[0], spam, strict=strict) for spam in data]
    )


def _parse_class(type_: type[T], data: dict[str, Any], *, strict: bool) -> T:
    """Parse data into a class."""
    # pylint: disable=too-complex
    signature = inspect.signature(type_.__init__)
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    in_positional = False

    def add(_name: str, _value: Any) -> None:
        if in_positional:
            args.append(_value)
        else:
            kwargs[_name] = _value

    first = True
    for arg_name, param in signature.parameters.items():
        if first:
            first = False
            continue
        if param.kind in {Parameter.VAR_KEYWORD, Parameter.KEYWORD_ONLY}:
            in_positional = True
        if arg_name not in data:
            if param.default == Parameter.empty:
                raise ValueError(f"Missing required argument {arg_name!r}")
            add(arg_name, param.default)
            continue
        value = data[arg_name]
        if param.annotation == Parameter.empty:
            if strict:
                raise ValueError(f"Missing type annotation for {arg_name!r}")
            add(arg_name, value)
            continue
        annotation = param.annotation
        if isinstance(annotation, str):
            annotation = type_.__init__.__annotations__.get(
                arg_name, annotation
            )
        add(arg_name, parse(annotation, value, strict=strict))

    return type_(*args, **kwargs)


def parse_args(
    *, type_: Any, name: str = "data"
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Insert kwarg with name and type into function."""

    def _inner(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def new_func(self: RequestHandler, *args: Any, **kwargs: Any) -> T:
            arguments: dict[str, str] = {}
            for key, values in self.request.arguments.items():
                if values:
                    arguments[key] = values[-1].decode("UTF-8")
            try:
                _data = parse(type_, arguments, strict=False)
            except ValueError as err:
                raise HTTPError(400, reason=err.args[0]) from err
            return func(self, *args, **kwargs, **{name: _data})

        return new_func

    return _inner
