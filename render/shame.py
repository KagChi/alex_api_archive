from io import BytesIO
from PIL import Image
from utils import http
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('shame', __name__)


async def create_shame(url):
    base = Image.open('assets/shame/under.png')
    overlay = Image.open('assets/shame/over.png')

    try:
        image = Image.open(BytesIO(await http.get(url, res_method="read"))).convert("RGBA")
        face = image.resize((240, 240))
    except Exception:
        abort(400, "Image URL is invalid...")

    base.paste(face, (680, 530), face)
    base.paste(overlay, (0, 0), overlay)

    bio = BytesIO()
    base.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/shame')
async def shame():
    """?image=url"""
    image = request.args.get('image')
    if not image:
        abort(400, "You must provide an image")

    return await send_file(
        await create_shame(image),
        mimetype='image/png',
        attachment_filename='shame.png'
    )
