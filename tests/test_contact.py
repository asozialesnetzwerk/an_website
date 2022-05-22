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

"""The tests for the contact page."""

from __future__ import annotations

import random

import orjson as json
import pytest
from envelope import Envelope  # type: ignore[import]
from tornado.httpclient import AsyncHTTPClient

from an_website import NAME
from an_website.contact import contact

from . import FetchCallable, app, fetch

assert fetch and app


def test_add_geoip_info_to_message() -> None:
    """Test the add_geoip_info_to_message function."""
    geoip = {
        "continent_name": "Oceania",
        "country_name": "Australia",
        "location": {"lon": 143.2104, "lat": -33.494},
        "country_iso_code": "AU",
        "timezone": "Australia/Sydney",
    }

    message = Envelope()
    contact.add_geoip_info_to_envelope(message, geoip)

    # pylint: disable=protected-access
    assert message._headers._headers == [
        ("X-GeoIP-continent-name", "Oceania"),
        ("X-GeoIP-country-name", "Australia"),
        ("X-GeoIP-location-lon", "143.2104"),
        ("X-GeoIP-location-lat", "-33.494"),
        ("X-GeoIP-country-iso-code", "AU"),
        ("X-GeoIP-timezone", "Australia/Sydney"),
    ]


def test_add_geoip_info_to_message_recursive() -> None:
    """Test infinite recursion."""
    geoip: dict[str, str | dict] = {"spam": "eggs"}  # type: ignore[type-arg]
    geoip["sausage"] = geoip
    env = Envelope()
    with pytest.raises(RecursionError):
        contact.add_geoip_info_to_envelope(env, geoip)


async def test_sending_email(
    # pylint: disable=redefined-outer-name
    fetch: FetchCallable,
) -> None:
    """Test sending emails."""
    name = random.randbytes(10).hex()
    subject = random.randbytes(10).hex()
    content = random.randbytes(80).hex()
    address = f"{random.randbytes(10).hex()}@{random.randbytes(5).hex()}.test"

    await fetch(
        "/kontakt",
        method="POST",
        body=json.dumps(
            {
                "nachricht": content,
                "name": name,
                "subjekt": subject,
                "addresse": address,
            }
        ),
    )

    response = await AsyncHTTPClient().fetch(
        f"https://restmail.net/mail/{NAME}"
    )

    for email in json.loads(response.body):
        if (  # pylint: disable=too-many-boolean-expressions
            email["subject"] == subject
            and email["text"] == f"{content}\n"
            and email["from"][0]["name"] == name
            and email["from"][0]["address"] == address
            and email["headers"]["from"] == f"{name} <{address}>"
            and email["headers"]["sender"] == "Marcell D'Avis <davis@1und1.de>"
            and not email["to"][0]["name"]
            and email["to"][0]["address"] == f"{NAME}@restmail.net"
            and email["headers"]["content-type"]
            == 'text/plain; charset="utf-8"'
        ):
            return
    raise AssertionError()
