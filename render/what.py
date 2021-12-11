from io import BytesIO
from PIL import Image
from utils import http
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('what', __name__)


async def create_what(url):
    base = Image.open('assets/what/what.png')
    background = Image.new("RGBA", base.size, (0, 0, 0, 255))

    try:
        image = Image.open(BytesIO(await http.get(url, res_method="read"))).convert("RGBA")
        face = image.resize((890, 710))
    except Exception:
        abort(400, "Image URL is invalid...")

    background.paste(face, (40, 40), face)
    background.paste(base, (0, 0), base)

    bio = BytesIO()
    background.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/what')
async def what():
    """?image=url"""
    image = request.args.get('image')
    if not image:
        abort(400, "You must provide an image")

    return await send_file(
        await create_what(image),
        mimetype='image/png',
        attachment_filename='what.png'
    )
