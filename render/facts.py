import textwrap

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('facts', __name__)


def create_facts(input):
    final_text = textwrap.fill(input, 22)
    b = BytesIO()

    base = Image.open("assets/facts/template.jpg").convert("RGBA")
    txtO = Image.new("RGBA", base.size, (255, 255, 255, 0))
    font = ImageFont.truetype("assets/_fonts/verdana_edited.ttf", 20)

    canv = ImageDraw.Draw(txtO)
    canv.text((65, 400), final_text, font=font, fill="Black")

    txtO = txtO.rotate(-15, resample=Image.BICUBIC)

    out = Image.alpha_composite(base, txtO)

    out.save(b, "PNG")
    b.seek(0)
    return b


@blueprint.route('/facts')
async def facts():
    """?text=text"""
    text = request.args.get('text')
    if not text:
        abort(400, "You must provide some text")

    if len(text) > 500:
        abort(400, "You are limited to 500 characters only, sorry")

    return await send_file(
        create_facts(text),
        mimetype='image/png',
        attachment_filename='facts.png'
    )
