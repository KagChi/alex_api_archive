from io import BytesIO
from PIL import Image
from utils import http
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('opinion', __name__)


async def create_trash(url, url_trash):
    avatarsize = 175

    base = Image.open('assets/trash/image.png')
    hand = Image.open("assets/trash/hand.png")

    try:
        image = Image.open(BytesIO(await http.get(url, res_method="read"))).convert("RGBA")
        face = image.resize((avatarsize, avatarsize))
        face = face.rotate(5, expand=True, resample=Image.BICUBIC)
    except Exception:
        abort(400, "Face URL is invalid...")

    try:
        trash = Image.open(BytesIO(await http.get(url_trash, res_method="read"))).convert("RGBA")
        trash_face = trash.resize((avatarsize, avatarsize))
    except Exception:
        abort(400, "Trash URL is invalid...")

    base.paste(face, (375, 80), face)
    base.paste(trash_face, (105, 190), trash_face)
    base.paste(hand, (156, 164), hand)

    bio = BytesIO()
    base.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/trash')
async def trash():
    """?face=url&trash=url"""
    face = request.args.get('face')
    trash = request.args.get('trash')

    if not face or not trash:
        abort(400, "You must provide both face and trash image.")

    return await send_file(
        await create_trash(face, trash),
        mimetype='image/png',
        attachment_filename='trash.png'
    )
