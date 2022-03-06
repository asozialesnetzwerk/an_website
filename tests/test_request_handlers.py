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

"""Test the request handlers of an_website."""


from __future__ import annotations

from collections.abc import Awaitable, Callable

import pytest
import tornado.escape
import tornado.httpclient
import tornado.web

from an_website import main

from . import (
    assert_valid_html_response,
    assert_valid_json_response,
    assert_valid_rss_response,
)


@pytest.fixture
def app() -> tornado.web.Application:
    """Create the application."""
    return main.make_app()  # type: ignore[return-value]


@pytest.fixture
def fetch(
    http_server_client: tornado.httpclient.AsyncHTTPClient,
) -> Callable[[str], Awaitable[tornado.httpclient.HTTPResponse]]:
    """Fetch a URL."""

    async def fetch_url(url: str) -> tornado.httpclient.HTTPResponse:
        """Fetch a URL."""
        return await http_server_client.fetch(url, raise_error=False)

    return fetch_url


async def test_json_apis(
    # pylint: disable=redefined-outer-name
    fetch: Callable[[str], Awaitable[tornado.httpclient.HTTPResponse]]
) -> None:
    """Check whether the APIs return valid JSON."""
    json_apis = (
        "/api/endpunkte",
        "/api/version",
        "/api/betriebszeit",
        "/api/discord",
        # "/api/discord/367648314184826880",  # needs network access
        # "/api/discord",  # needs network access
        # "/api/zitate/1-1",  # gets tested with quotes
        "/api/hangman-loeser",
        # "/api/ping",  # (not JSON)
        # "/api/restart",  # (not 200)
        "/api/vertauschte-woerter",
        "/api/wortspiel-helfer",
        "/api/waehrungs-rechner",
    )
    for api in json_apis:
        assert_valid_json_response(await fetch(api))


async def test_request_handlers(
    # pylint: disable=redefined-outer-name, too-many-statements
    fetch: Callable[[str], Awaitable[tornado.httpclient.HTTPResponse]]
) -> None:
    """Check if the request handlers return 200 codes."""
    response = await fetch("/")
    assert response.code == 200
    for theme in ("default", "blue", "random", "random-dark"):
        assert_valid_html_response(await fetch(f"/?theme={theme}"))
    for _b1, _b2 in (("sure", "true"), ("nope", "false")):
        response = await fetch(f"/?no_3rd_party={_b1}")
        body = response.body.decode()
        assert_valid_html_response(response)
        response = await fetch(f"/?no_3rd_party={_b2}")
        assert_valid_html_response(response)
        assert response.body.decode().replace(_b2, _b1) == body
    assert_valid_html_response(await fetch("/?c=s"))
    response = await fetch("/redirect?from=/&to=https://example.org")
    assert_valid_html_response(response)
    assert b"https://example.org" in response.body

    response = await fetch("/robots.txt")
    assert response.code == 200
    response = await fetch("/favicon.ico")
    assert response.code == 200
    response = await fetch("/static/robots.txt")
    assert response.code == 200
    response = await fetch("/static/favicon.ico")
    assert response.code == 200

    assert_valid_html_response(await fetch("/betriebszeit"))
    assert_valid_html_response(await fetch("/version"))
    assert_valid_html_response(await fetch("/suche"))
    assert_valid_html_response(await fetch("/kaenguru-comics"))
    assert_valid_html_response(await fetch("/hangman-loeser"))
    assert_valid_html_response(await fetch("/wortspiel-helfer"))
    assert_valid_html_response(await fetch("/services"))
    assert_valid_html_response(await fetch("/vertauschte-woerter"))
    assert_valid_html_response(await fetch("/waehrungs-rechner"))
    assert_valid_html_response(await fetch("/host-info"))
    assert_valid_html_response(await fetch("/einstellungen"))
    assert_valid_html_response(await fetch("/wiki"))
    assert_valid_html_response(await fetch("/js-lizenzen"))
    assert_valid_html_response(await fetch("/endpunkte"))
    assert_valid_html_response(await fetch("/soundboard"))
    assert_valid_html_response(await fetch("/soundboard/personen"))
    assert_valid_html_response(await fetch("/soundboard/suche"))

    await fetch("/host-info/uwu")
    assert response.code in {200, 501}
    # assert_valid_html_response(response, response.code)

    assert_valid_rss_response(await fetch("/soundboard/feed"))
    assert_valid_rss_response(await fetch("/soundboard/muk/feed"))

    assert_valid_html_response(await fetch("/soundboard/muk"))
    assert_valid_html_response(await fetch("/soundboard/qwertzuiop/feed"), 404)
    assert_valid_html_response(await fetch("/soundboard/qwertzuiop"), 404)

    assert_valid_json_response(await fetch("/api/restart"), 401)
    response = await fetch("/api/backdoor/eval")
    assert response.code == 401  # Unauthorized
    response = await fetch("/api/backdoor/exec")
    assert response.code == 401  # Unauthorized

    response = await fetch("/api/ping")
    assert response.code == 200
    assert response.body.decode() == "🏓"

    for code in range(200, 599):
        if code not in (204, 304):
            assert_valid_html_response(await fetch(f"/{code}.html"), code)
    assert_valid_html_response(await fetch("/qwertzuiop"), 404)
