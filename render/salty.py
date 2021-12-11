from io import BytesIO
from PIL import Image
from utils import http
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('salty', __name__)


async def create_salty(url):
    salt_size = 100

    base = Image.new("RGBA", (128, 128 + salt_size))

    try:
        image = Image.open(BytesIO(await http.get(url, res_method="read"))).convert("RGBA")
        face = image.resize((128, 128))
    except Exception:
        abort(400, "Image URL is invalid...")

    salt = Image.open('assets/salty/salt.png')
    salt_re = salt.resize((salt_size, salt_size))

    base.paste(face, (0, salt_size), face)
    base.paste(salt_re, (128 - salt_size, 2), salt_re)

    bio = BytesIO()
    base.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/salty')
async def salty():
    """?image=url"""
    image = request.args.get('image')
    if not image:
        abort(400, "You must provide an image")

    return await send_file(
        await create_salty(image),
        mimetype='image/png',
        attachment_filename='salty.png'
    )
