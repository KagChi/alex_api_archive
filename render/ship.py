from utils import http
from io import BytesIO
from PIL import Image
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('ship', __name__)


async def gen_ship(user, user2):
    base = Image.new("RGBA", (3 * 128, 128))
    av = Image.open(BytesIO(await http.get(user, res_method="read"))).convert("RGBA")
    av2 = Image.open(BytesIO(await http.get(user2, res_method="read"))).convert("RGBA")

    av = av.resize((128, 128))
    av2 = av2.resize((128, 128))
    mid = Image.open("assets/images/heart.png")

    base.paste(av, (0, 0))
    base.paste(mid, (128, 0))
    base.paste(av2, (256, 0))

    b = BytesIO()
    base.save(b, 'PNG')
    b.seek(0)
    return b


@blueprint.route('/ship')
async def ship():
    """?user=url&user2=url"""
    user = request.args.get('user')
    user2 = request.args.get('user2')

    if not user or not user2:
        abort(400, "You must provide 2 user URLs")

    return await send_file(
        await gen_ship(user, user2),
        mimetype='image/png',
        attachment_filename='joketoyou.png'
    )
