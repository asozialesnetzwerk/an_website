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

"""Module that generates an image from a wrong quote."""
from __future__ import annotations

import io
import textwrap

from PIL import Image, ImageDraw, ImageFont

from . import DIR, QuoteReadyCheckRequestHandler, get_wrong_quote

AUTHOR_MAX_WIDTH: int = 686
QUOTE_MAX_WIDTH: int = 900
TEXT_COLOR: tuple[int, int, int] = 230, 230, 230
FONT = ImageFont.truetype(
    font=f"{DIR}/files/oswald.regular.ttf",
    size=50,
)
HOST_NAME_FONT = ImageFont.truetype(
    font=f"{DIR}/files/oswald.regular.ttf",
    size=23,
)

BG_IMG = Image.open(f"{DIR}/files/bg.png", formats=("PNG",))
IMAGE_WIDTH, IMAGE_HEIGHT = BG_IMG.size
WITZIG_IMG = Image.open(f"{DIR}/files/StempelWitzig.png", formats=("PNG",))
NICHT_WITZIG_IMG = Image.open(
    f"{DIR}/files/StempelNichtWitzig.png", formats=("PNG",)
)


def get_lines_and_max_height(
    text: str, max_width: int
) -> tuple[list[str], int]:
    """Get the lines of the text and the max line height."""
    column_count = 42
    lines: list[str] = []

    max_line_length = max_width + 1
    while max_line_length > max_width:
        lines = textwrap.wrap(text, width=column_count)
        max_line_length = max(FONT.getsize(line)[0] for line in lines)
        column_count -= 1

    return lines, max(FONT.getsize(line)[1] for line in lines)


def draw_text(
    img: ImageDraw.ImageDraw,
    text: str,
    _x: int,
    _y: int,
    font: ImageFont.FreeTypeFont = FONT,
):
    """Draw a text on an image."""
    img.text(
        (_x, _y),
        text,
        font=font,
        fill=TEXT_COLOR,
        align="right",
        spacing=54,
    )


def draw_lines(
    img: ImageDraw.ImageDraw,
    lines: list[str],
    y_start: int,
    max_w: int,
    max_h: int,
) -> int:
    """Draw the lines on the image and return the last y position."""
    for line in lines:
        width = FONT.getsize(line)[0]
        draw_text(
            img=img,
            text=line,
            _x=(max_w - width) // 2,
            _y=y_start,
        )
        y_start += max_h
    return y_start


def create_image(  # pylint: disable=too-many-locals
    quote: str, author: str, rating: int, host_name: str
):
    """Create an image with the given quote and author."""
    img = BG_IMG.copy()
    draw = ImageDraw.Draw(img, mode="RGBA")

    # draw quote
    quote_lines, max_line_height = get_lines_and_max_height(
        f"»{quote}«", QUOTE_MAX_WIDTH
    )
    if len(quote_lines) < 3:
        y_start = 175
    elif len(quote_lines) < 4:
        y_start = 125
    else:
        y_start = 75
    y_text = draw_lines(
        draw,
        quote_lines,
        y_start,
        QUOTE_MAX_WIDTH,
        max_line_height,
    )

    # draw author
    author = f"- {author}"
    width, max_line_height = FONT.getsize(author)
    if width <= AUTHOR_MAX_WIDTH:
        author_lines = [author]
    else:
        author_lines, max_line_height = get_lines_and_max_height(
            author, AUTHOR_MAX_WIDTH
        )
    draw_lines(
        draw,
        author_lines,
        max(y_text + 20, IMAGE_HEIGHT - 220),
        AUTHOR_MAX_WIDTH,
        max_line_height,
    )

    # draw rating
    if rating != 0:
        width, height = FONT.getsize(str(rating))
        y_rating = IMAGE_HEIGHT - 25 - height
        draw_text(
            img=draw,
            text=str(rating),
            _x=25,
            _y=y_rating,
        )
        # draw rating img
        icon = NICHT_WITZIG_IMG if rating < 0 else WITZIG_IMG
        img.paste(
            icon,
            box=(
                25 + 5 + width,
                y_rating + 8,  # 8 is a magic number, that makes it look good
            ),
            mask=icon,
        )

    # draw host name
    width, height = HOST_NAME_FONT.getsize(host_name)
    draw_text(
        img=draw,
        text=host_name,
        _x=IMAGE_WIDTH - 5 - width,
        _y=IMAGE_HEIGHT - 5 - height,
        font=HOST_NAME_FONT,
    )
    io_buf = io.BytesIO()
    img.save(
        io_buf,
        format="PNG",
    )
    return io_buf.getvalue()


class QuoteAsImg(QuoteReadyCheckRequestHandler):
    """Quote as img request handler."""

    RATELIMIT_TOKENS = 3

    async def get(self, quote_id: str, author_id: str):
        """Handle the get request to this page and render the quote as img."""
        wrong_quote = await get_wrong_quote(int(quote_id), int(author_id))
        self.request.host_name = "asozial.net"
        _id = (
            wrong_quote.id
            if wrong_quote.id != -1
            else f"{quote_id}-{author_id}"
        )
        self.set_header("Content-Type", "image/png")
        await self.finish(
            create_image(
                wrong_quote.quote.quote,
                wrong_quote.author.name,
                wrong_quote.rating,
                f"{self.request.host_name}/z/{_id}",
            )
        )
