from io import BytesIO
from PIL import Image
from utils import http
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('amiajoke', __name__)


async def create_bad(url):
    base = Image.open('assets/amiajoke/joke.jpg')
    bg = Image.new("RGBA", (276, 276), (0, 0, 0))

    try:
        image = Image.open(BytesIO(await http.get(url, res_method="read"))).convert("RGBA")
        face = image.resize((276, 276))
    except Exception:
        abort(400, "Image URL is invalid...")

    base.paste(bg, (335, 35), bg)
    base.paste(face, (335, 35), face)

    bio = BytesIO()
    base.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/amiajoke')
async def amiajoke():
    """?image=url"""
    image = request.args.get('image')
    if not image:
        abort(400, "You must provide an image")

    return await send_file(
        await create_bad(image),
        mimetype='image/png',
        attachment_filename='joketoyou.png'
    )
