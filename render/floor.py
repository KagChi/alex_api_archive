import textwrap

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from quart import Blueprint, request, send_file, abort
from utils import http

blueprint = Blueprint('floor', __name__)


async def create_floor_meme(text: str, image: str):
    meme_format = Image.open('assets/floor/floor.png')

    # == Text ==
    fnt = ImageFont.truetype('assets/_fonts/Arial.ttf', 30)
    d = ImageDraw.Draw(meme_format)

    margin = 20
    offset = 25
    for line in textwrap.wrap(f'The floor is {text}', width=65):
        d.text((margin, offset), line, font=fnt, fill=(0,) * 3)
        offset += fnt.getsize(line)[1]

    if image:
        # == Avatars ==
        try:
            image = Image.open(BytesIO(await http.get(image, res_method="read")))
        except Exception:
            abort(400, "Image URL is invalid...")

        first = image.resize((20, 20))
        second = image.resize((40, 40))

        meme_format.paste(first, (143, 135))
        meme_format.paste(second, (465, 133))

    return meme_format


async def floor_render(text: str, image: str):
    text = text.replace("\n", "")
    im = await create_floor_meme(text, image)
    bio = BytesIO()
    im.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/floor')
async def floor():
    """?image=url&text=text"""
    image = request.args.get('image')
    text = request.args.get('text')

    if not text:
        abort(400, "Invalid input to text")

    if len(text) > 179:
        abort(400, "Your text input is too long")

    return await send_file(
        await floor_render(text, image),
        mimetype='image/png',
        attachment_filename='the_floor.png'
    )
