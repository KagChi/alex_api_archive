from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('pornhub', __name__)


def create_pornhub(text: str, text2: str, iwidth: int = 16, height: int = 161, padding: int = 10, fontsize: int = 164):
    txt = Image.new("RGBA", (len(text) * 15, height))
    txt2 = Image.new("RGBA", (len(text2) * 15, height))

    fnt = ImageFont.truetype("assets/_fonts/ArialB.ttf", fontsize)
    d = ImageDraw.Draw(txt)
    w, h = d.textsize(text, font=fnt)
    w2, h2 = d.textsize(text2, font=fnt)

    textwindow_size = w + w2 + padding + (iwidth * 2)

    mid = Image.new("RGBA", (w, height), (255, 255, 255, 0))
    mid2 = Image.new("RGBA", (w2 + iwidth, height), (255, 255, 255, 0))

    midd_t = Image.new("RGBA", (1, height), (255, 255, 255, 0))
    start = Image.open("assets/pornhub/pornstart.png")
    midd = Image.open("assets/pornhub/pornmid.png")
    end = Image.open("assets/pornhub/pornend.png")

    for i in range(0, w):
        mid.paste(midd_t, (i, 0))

    for i in range(0, w2):
        mid2.paste(midd, (i, 0))
    mid2.paste(end, (w2, 0))

    txt = Image.new("RGBA", (textwindow_size, height), (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)

    middle_align = -10
    d.text((0, middle_align), text, font=fnt, fill=(255, 255, 255, 255))
    d.text((w + iwidth + padding, middle_align), text2, font=fnt, fill=(0, 0, 0, 255))

    im = Image.new("RGBA", (textwindow_size, height), (255, 255, 255, 0))

    im.paste(mid, (0, 0))
    im.paste(start, (w + padding, 0))
    im.paste(mid2, (w + iwidth + padding, 0))
    im.paste(txt, (0, 0), txt)
    im.paste(txt2, (w + iwidth + padding, 0), txt2)

    bio = BytesIO()
    im.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/pornhub')
async def pornhub():
    """?text=text&text2=text"""
    text = request.args.get('text')
    text2 = request.args.get('text2')

    if not text or not text2:
        abort(400, "You must provide both text and text2")

    if len(text + text2) > 500:
        abort(400, "You can't use more than 500 characters, sorry.")

    return await send_file(
        create_pornhub(text, text2),
        mimetype='image/png',
        attachment_filename='bad.png'
    )
