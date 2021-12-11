import random

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from quart import Blueprint, request, send_file, abort, jsonify

blueprint = Blueprint('achievement', __name__)

helper_icons = {
    "1": "Grass block", "2": "Diamond", "3": "Diamond sword",
    "4": "Creeper", "5": "Pig", "6": "TNT",
    "7": "Cookie", "8": "Heart", "9": "Bed",
    "10": "Cake", "11": "Sign", "12": "Rail",
    "13": "Crafting bench", "14": "Redstone", "15": "Fire",
    "16": "Cobweb", "17": "Chest", "18": "Furnace",
    "19": "Book", "20": "Stone block", "21": "Wooden plank block",
    "22": "Iron ingot", "23": "Gold ingot", "24": "Wooden door",
    "25": "Iron Door", "26": "Diamond chestplate", "27": "Flint and steel",
    "28": "Glass bottle", "29": "Splash potion", "30": "Creeper spawnegg",
    "31": "Coal", "32": "Iron sword", "33": "Bow",
    "34": "Arrow", "35": "Iron chestplate", "36": "Bucket",
    "37": "Bucket with water", "38": "Bucket with lava", "39": "Bucket with milk",
    "40": "Diamond boots", "41": "Wooden hoe", "42": "Bread", "43": "Wooden sword",
    "44": "Bone", "45": "Oak log"
}


def create_achievement(title: str, ach: str, colour=(255, 255, 0, 255), icon: int = None):
    randomimage = icon if icon else random.randint(1, 45)
    front = Image.open(f"assets/achievement/{randomimage}.png")

    txt = Image.new("RGBA", (len(ach) * 15, 64))

    fnt = ImageFont.truetype('assets/_fonts/Minecraft.ttf', 16)
    d = ImageDraw.Draw(txt)

    w, h = d.textsize(ach, font=fnt)
    w = max(320, w)

    mid = Image.new("RGBA", (w + 20, 64), (255, 255, 255, 0))

    midd = Image.open("assets/achievement/achmid.png")
    end = Image.open("assets/achievement/achend.png")

    for i in range(0, w):
        mid.paste(midd, (i, 0))
    mid.paste(end, (w, 0))

    txt = Image.new("RGBA", (w + 20, 64), (255, 255, 255, 0))

    d = ImageDraw.Draw(txt)
    d.text((0, 9), title, font=fnt, fill=colour)
    d.text((0, 29), ach, font=fnt, fill=(255, 255, 255, 255))

    mid = Image.alpha_composite(mid, txt)

    im = Image.new("RGBA", (w + 80, 64))

    im.paste(front, (0, 0))
    im.paste(mid, (60, 0))

    bio = BytesIO()
    im.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route("/achievement")
async def achievement():
    """?text=text[&icon=int]"""
    text = request.args.get('text')
    icon = request.args.get('icon')

    try:
        if icon:
            if int(icon) in range(1, 46):
                icon = int(icon)
            else:
                return jsonify(helper_icons)
        else:
            icon = 0
    except ValueError:
        abort(400, "Icon can only be int")

    if not text:
        abort(400, "You are required to define text.")

    if len(text) > 500:
        abort(400, "You shouldn't make the achievement over 500 characters long...")

    return await send_file(
        create_achievement("Achievement Get!", text, icon=icon),
        mimetype="image/png",
        attachment_filename="achievement.png"
    )


@blueprint.route("/challenge")
async def challenge():
    """?text=text[&icon=int]"""
    text = request.args.get('text')
    icon = request.args.get('icon')

    try:
        if icon:
            if int(icon) in range(1, 46):
                icon = int(icon)
            else:
                return jsonify(helper_icons)
        else:
            icon = 0
    except ValueError:
        abort(400, "Icon can only be int")

    if not text:
        abort(400, "You are required to define text.")

    if len(text) > 500:
        abort(400, "You shouldn't make the achievement over 500 characters long...")

    return await send_file(
        create_achievement("Challenge Complete!", text, icon=icon, colour=(255, 128, 250)),
        mimetype="image/png",
        attachment_filename="achievement.png"
    )
