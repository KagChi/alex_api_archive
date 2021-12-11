import textwrap

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('scroll', __name__)


def create_scroll(content):
    f_text = textwrap.fill(content, 10)

    if len(f_text.split("\n")) > 6:
        return "Too many lines", 400

    base = Image.open("assets/sot/template.jpg").convert("RGBA")
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))
    font = ImageFont.truetype("assets/_fonts/verdana_edited.ttf", 15)

    canv = ImageDraw.Draw(txtO)
    canv.text((95, 283), f_text, font=font, fill="Black")

    txtO = txtO.rotate(2, resample=Image.BICUBIC)
    out = Image.alpha_composite(base, txtO)

    b = BytesIO()
    out.save(b, "PNG")
    b.seek(0)
    return b


@blueprint.route('/scroll')
async def scroll():
    """?text=text"""
    text = request.args.get('text')
    if not text:
        abort(400, "You must provide text")

    try:
        return await send_file(
            create_scroll(text),
            mimetype='image/png',
            attachment_filename='scroll_of_truth.png'
        )
    except TypeError:
        abort(400, f"You put in too many characters ({len(text)})")
