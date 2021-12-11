from io import BytesIO
from PIL import Image
from utils import http
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('jokeoverhead', __name__)


async def create_jokeoverhead(url):
    base = Image.open('assets/joke/thejoke.png')
    back = Image.new("RGBA", base.size, (0, 0, 0, 0))

    try:
        image = Image.open(BytesIO(await http.get(url, res_method="read"))).convert("RGBA")
        face = image.resize((138, 138))
    except Exception:
        abort(400, "Image URL is invalid...")

    bg = Image.new("RGBA", face.size, (0, 0, 0))

    facepos = (127, 125)
    back.paste(bg, facepos, bg)
    back.paste(face, facepos, face)
    back.paste(base, (0, 0), base)

    bio = BytesIO()
    back.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/jokeoverhead')
async def jokeoverhead():
    """?image=url"""
    image = request.args.get('image')
    if not image:
        abort(400, "You must provide an image")

    return await send_file(
        await create_jokeoverhead(image),
        mimetype='image/png',
        attachment_filename='joketoyou.png'
    )
