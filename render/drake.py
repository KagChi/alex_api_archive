import textwrap

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('drake', __name__)


def create_drake(top, bottom, image_template: str = None):
    top_text = textwrap.fill(top, 13)
    bottom_text = textwrap.fill(bottom, 13)

    b = BytesIO()
    template_use = image_template if image_template else 'template.jpg'
    base = Image.open(f"assets/drake/{template_use}").convert("RGBA")
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))
    font = ImageFont.truetype("assets/_fonts/verdana_edited.ttf", 35)

    top_pos = 85 + (-12 * len(top_text.split("\n")) + 10)
    bottom_pos = 335 + (-12 * len(bottom_text.split("\n")) + 10)

    canv = ImageDraw.Draw(txtO)
    canv.text((250, top_pos), top_text, font=font, fill="Black")
    canv.text((250, bottom_pos), bottom_text, font=font, fill="Black")

    out = Image.alpha_composite(base, txtO)

    out.save(b, "PNG")
    b.seek(0)
    return b


@blueprint.route('/drake')
async def drake():
    """?top=text&bottom=text"""
    top = request.args.get('top')
    bottom = request.args.get('bottom')
    ayano = request.args.get('ayano')
    if not top or not bottom:
        abort(400, "You must provide top and bottom text")

    if len(top + bottom) > 500:
        abort(400, "You are limited to 500 characters only, sorry")

    image_template = None
    if ayano:
        image_template = "template_ayano.jpg"

    return await send_file(
        create_drake(top, bottom, image_template=image_template),
        mimetype='image/png',
        attachment_filename='drake.png'
    )
