from io import BytesIO
from PIL import Image
from utils import http
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('bad', __name__)


async def create_bad(url):
    base = Image.open('assets/bad/bad.jpg')

    try:
        image = Image.open(BytesIO(await http.get(url, res_method="read"))).convert("RGBA")
        face = image.resize((128, 128))
    except Exception:
        abort(400, "Image URL is invalid...")

    base.paste(face, (50, 215), face)

    bio = BytesIO()
    base.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/bad')
async def bad():
    """?image=url"""
    image = request.args.get('image')
    if not image:
        abort(400, "You must provide an image")

    return await send_file(
        await create_bad(image),
        mimetype='image/png',
        attachment_filename='bad.png'
    )
