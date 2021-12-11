from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('captcha', __name__)


def create_captcha(text):
    front = Image.open("assets/captcha/start.png")

    txt = Image.new("RGBA", (len(text) * 15, 189))

    fnt = ImageFont.truetype('assets/_fonts/Roboto.ttf', 30)
    d = ImageDraw.Draw(txt)

    w, h = d.textsize(text, font=fnt)
    w = max(450, w)

    mid = Image.new("RGBA", (w + 201, 189), (255, 255, 255, 0))

    midd = Image.open("assets/captcha/mid.png")
    end = Image.open("assets/captcha/end.png")

    for i in range(0, w):
        mid.paste(midd, (i, 0))
    mid.paste(end, (w, 0))

    txt = Image.new("RGBA", (w + 201, 189), (255, 255, 255, 0))

    d = ImageDraw.Draw(txt)
    d.text((10, 73), text, font=fnt, fill=(0, 0, 0, 255))

    mid = Image.alpha_composite(mid, txt)

    im = Image.new("RGBA", (w + 323, 189))

    im.paste(front, (0, 0))
    im.paste(mid, (122, 0))

    bio = BytesIO()
    im.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/captcha')
async def captcha():
    """?text=text"""
    text = request.args.get('text')
    if not text:
        abort(400, "You must provide some text")

    if len(text) > 500:
        abort(400, "You are limited to 500 characters only, sorry")

    return await send_file(
        create_captcha(text),
        mimetype='image/png',
        attachment_filename='captcha.png'
    )
