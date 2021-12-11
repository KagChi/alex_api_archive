import textwrap

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('calling', __name__)


def create_calling(text):
    final_text = textwrap.fill(text, 33)
    b = BytesIO()

    base = Image.open("assets/calling/template.jpg").convert("RGBA")
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))
    font = ImageFont.truetype("assets/_fonts/verdana_edited.ttf", 35)

    canv = ImageDraw.Draw(txtO)
    canv.text((5, 5), final_text, font=font, fill="Black")

    out = Image.alpha_composite(base, txtO)

    out.save(b, "PNG")
    b.seek(0)
    return b


@blueprint.route('/calling')
async def calling():
    """?text=text"""
    text = request.args.get('text')
    if not text:
        abort(400, "You must provide text")

    if len(text) > 500:
        abort(400, "You are limited to 500 characters only, sorry")

    return await send_file(
        create_calling(text),
        mimetype='image/png',
        attachment_filename='calling.png'
    )
