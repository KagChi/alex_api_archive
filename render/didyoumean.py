from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('didyoumean', __name__)


def create_didyoumean(top: str, bottom: str):
    template = Image.open('assets/didyoumean/bg.png')
    imsize = (1302, 316)

    # == Text ==
    txt = Image.new("RGBA", imsize)

    fnt = ImageFont.truetype('assets/_fonts/Arial.ttf', 35)
    fntBI = ImageFont.truetype('assets/_fonts/ArialBI.ttf', 35)
    d = ImageDraw.Draw(txt)
    d.text((45, 41), top, font=fnt, fill=(0, 0, 0, 255))
    d.text((295, 250), bottom, font=fntBI, fill=(26, 13, 171, 255))
    d = ImageDraw.Draw(txt)

    im = Image.new("RGBA", imsize)

    im.paste(template, (0, 0))
    im.paste(txt, (0, 0), txt)
    return im


def didyoumean_render(top: str, bottom: str):
    top = top.replace("\n", "")
    bottom = bottom.replace("\n", "")

    im = create_didyoumean(top, bottom)
    bio = BytesIO()
    im.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/didyoumean')
async def didyoumean():
    """?top=text&bottom=text"""
    top = request.args.get('top')
    bottom = request.args.get('bottom')

    if not top or not bottom:
        abort(400, "You must include both top and bottom")

    if len(top) > 45:
        abort(400, "Your top input is too long [ Limit: 45 ]")

    if len(bottom) > 40:
        abort(400, "Your bottom input is too long [ Limit: 40 ]")

    return await send_file(
        didyoumean_render(top, bottom),
        mimetype='image/png',
        attachment_filename='the_floor.png'
    )
