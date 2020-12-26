from flask import Blueprint, request, jsonify
import requests, json

from utils import parser, fast_requests
from constants import AUTHORIZATION_CODE, INTRA_API_URL
import authorization

bp = Blueprint('forty_two', __name__, url_prefix='/42')

s = requests.Session()

@bp.route('/<path:path>', methods=['GET'])
def forty_two(path: str):
    header_authorization_code = request.headers.get("Authorization")
    if AUTHORIZATION_CODE == header_authorization_code:
        url = f"{INTRA_API_URL}/v2/{path}?{request.query_string.decode()}"
        page = request.args.get("page")
        try:
            r = s.get(url, headers=authorization.get_token_headers())
            r.raise_for_status()
            if page and "all" in page:
                data = []
                pages = parser.headers.get_pages(r.headers)
                urls = parser.url.all_pages(url, pages, fast=True)
                data = fast_requests.get.make_requests(urls)
                return jsonify(data), 200
            else:
                return jsonify(r.json()), 200
        except ConnectionError as e:
            return {"Failed": "Couldn't established connection with 42 API."}, 500
        except requests.HTTPError as e:
            if r.headers["Content-Type"] == "application/json":
                return jsonify(r.json()), r.status_code
            return {}, r.status_code
        except requests.Timeout as e:
            return {"Failed": "Timeout."}, 429
        except requests.TooManyRedirects as e:
            return {"Failed": "Exceed limit of redirects."}, 502
    else:
        return {"Failed": "You need provide a valid authorization code."}, 401
