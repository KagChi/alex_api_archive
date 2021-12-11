import os
import wand
import wand.image
import random

from io import BytesIO
from utils import http
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageSequence
from quart import Blueprint, request, send_file, abort, jsonify

blueprint = Blueprint('filter', __name__)


def create_filter(face, filter, size):
    width, height = size

    if filter == "blur":
        face = face.filter(ImageFilter.GaussianBlur(radius=2.5))
    elif filter == "invert":
        r, g, b, a = face.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        face = ImageOps.invert(rgb_image)
    elif filter == "flip":
        face = face.rotate(180)
    elif filter == "mirror":
        face = ImageOps.mirror(face)
    elif filter == "pixelate":
        img_size = face.size

        sat_booster = ImageEnhance.Color(face)
        face = sat_booster.enhance(float(1.25))
        contr_booster = ImageEnhance.Contrast(face)
        face = contr_booster.enhance(float(1.2))
        face = face.convert('P', palette=Image.ADAPTIVE)

        superpixel_size = 10
        reduced_size = (img_size[0] // superpixel_size, img_size[1] // superpixel_size)

        face = face.resize(reduced_size, Image.BICUBIC)
        face = face.resize(img_size, Image.ANTIALIAS)
    elif filter == "jpegify":
        final = BytesIO()
        face.convert("RGB").save(final, 'JPEG', quality=random.randint(1, 11))
    elif filter == "b&w":
        face = face.convert('L')
    elif filter == "sepia":
        pixels = face.load()
        for py in range(height):
            for px in range(width):
                r, g, b, a = face.getpixel((px, py))
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                if tr > 255:
                    tr = 255
                if tg > 255:
                    tg = 255
                if tb > 255:
                    tb = 255

                pixels[px, py] = (tr, tg, tb)
    elif filter == "deepfry":
        img = face.convert('RGB')
        img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
        img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
        img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
        img = img.resize((width, height), resample=Image.BICUBIC)
        img = ImageOps.posterize(img, 4)

        r = img.split()[0]
        r = ImageEnhance.Contrast(r).enhance(2.0)
        r = ImageEnhance.Brightness(r).enhance(1.5)

        r = ImageOps.colorize(r, (254, 0, 2), (255, 255, 15))

        img = Image.blend(img, r, 0.75)
        face = ImageEnhance.Sharpness(img).enhance(100.0)
    elif filter == "wide":
        face = face.filter(ImageFilter.GaussianBlur(radius=1.5))
        face = face.resize((
            int(width * 1.25), int(height / 1.5)
        ))
    else:
        try:
            base = Image.open(f'assets/filter/{filter}.png')
            filtered = base.resize((width, height))
            face.paste(filtered, (0, 0), filtered)
        except FileNotFoundError:
            abort(404, "Filter not found")

    return face


async def render_filter(url, filter: str):
    """ Render the image """
    try:
        im = Image.open(BytesIO(await http.get(url, res_method="read")))
        width, height = im.size
    except Exception:
        abort(400, "Image URL is invalid...")

    try:
        isgif = True
        int(im.info["loop"])
    except Exception:
        isgif = False

    if isgif:
        frames = [g.copy() for g in ImageSequence.Iterator(im)]

        if len(frames) > 150 and filter in ["sepia"]:
            return abort(400, f"Too many frames on GIF to render {filter}...")

        frame_durations = []
        newgif = []
        for frame in frames:
            frame = frame.convert(mode='RGBA')
            frame_durations.append(im.info.get('duration', 1))
            render = create_filter(frame, filter, (width, height))
            newgif.append(render)

        image_file_object = BytesIO()
        gif = newgif[0]
        gif.save(
            image_file_object, format="gif", save_all=True,
            append_images=newgif[1:], loop=0, duration=frame_durations,
            transparency=0, disposal=2
        )
        image_file_object.seek(0)
        return (image_file_object, "gif")
    else:
        render = create_filter(im.convert("RGBA"), filter, (width, height))
        bio = BytesIO()
        render.save(bio, "PNG")
        bio.seek(0)
        return (bio, "png")


@blueprint.route('/filter')
async def filter_home():
    all_filters = [
        "blur", "invert", "b&w", "deepfry", "sepia",
        "pixelate", "jpegify", "wide", "flip",
        "mirror"
    ]

    for file in os.listdir("assets/filter"):
        name = file.split(".")
        all_filters.append(name[0])

    return jsonify([f"GET filter/{g}?<image:url>" for g in all_filters])


@blueprint.route('/filter/<overlay>')
async def filter(overlay):
    image = request.args.get('image')
    if not image:
        abort(400, "You must provide an image")

    upload_image, img_format = await render_filter(image, overlay)

    return await send_file(
        upload_image,
        mimetype=f'image/{img_format}',
        attachment_filename=f'filter.{img_format}'
    )
