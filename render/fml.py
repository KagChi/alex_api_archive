from bs4 import BeautifulSoup
from quart import Blueprint, jsonify
from utils import http

blueprint = Blueprint('fml', __name__)


@blueprint.route("/fml", methods=['GET'])
async def fml():
    resp = await http.get(
        "https://www.fmylife.com/random", res_method="read",
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    )

    page = BeautifulSoup(resp, 'html.parser')
    posts = page.find_all('a', class_='block text-blue-500 my-4')

    return jsonify({
        "text": posts[0].get_text().strip()
    })
