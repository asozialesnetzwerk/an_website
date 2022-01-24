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

"""The page that generates art."""
from __future__ import annotations

from tornado.web import HTTPError

from ..utils.request_handler import BaseRequestHandler
from ..utils.utils import ModuleInfo


def get_module_info() -> ModuleInfo:
    """Create and return the ModuleInfo for this module."""
    return ModuleInfo(
        handlers=((r"/lolwut/", LOLWUT), (r"/lolwut/([0-9/]+)/", LOLWUT)),
        name="LOLWUT",
        description="LOLWUT; präsentiert von Redis",
        path="/lolwut/",
        keywords=(
            "LOLWUT",
            "Redis",
        ),
    )


class LOLWUT(BaseRequestHandler):
    """The request handler for the LOLWUT page."""

    async def get(self, args: str = "") -> None:
        """Handle GET requests to the LOLWUT page."""
        if args:
            arguments = args.split("/")
            if not len(arguments) == 1 and not arguments[-1]:
                arguments = arguments[:-1]
            for argument in arguments:
                if not argument:
                    raise HTTPError(404)
            command = "LOLWUT VERSION " + " ".join(arguments)
        else:
            command = "LOLWUT"
        if not self.redis:
            raise HTTPError(503)
        await self.render(
            "pages/ansi2html.html",
            ansi=await self.redis.execute_command(command),  # type: ignore
            powered_by="https://redis.io",
            powered_by_name="Redis",
        )
