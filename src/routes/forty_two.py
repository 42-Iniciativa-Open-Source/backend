from flask import Blueprint, request, jsonify
import requests

import threading_requests.get

import parser.headers, parser.url
from constants import AUTHORIZATION_CODE, INTRA_API_URL
import authorization

bp = Blueprint('forty_two', __name__, url_prefix='/42')

@bp.route('/<path:path>', methods=['GET'])
def forty_two(path: str):
    header_authorization_code = request.headers.get("Authorization")
    if AUTHORIZATION_CODE == header_authorization_code:
        page = request.args.get("page")
        url = f"{INTRA_API_URL}/v2/{path}?{request.query_string.decode()}"
        try:
            if page == "all":
                data = []
                urls = []
                page = 1
                url = parser.url.rename_query_string(url, {"page": "page[number]"})
                url = parser.url.set_query_string(url, {"page[number]": page, "page[size]": 100})
                r = requests.get(url, headers=authorization.get_token_headers())
                r.raise_for_status()
                pages = parser.headers.get_pages(r.headers)
                for page in range(1, int(pages["last"])):
                    url = parser.url.set_query_string(url, {"page[number]": page})
                    urls.append(url)
                print(urls, len(urls))
                print(threading_requests.get.get(urls))
                return jsonify(urls), 200
                #return jsonify(data), 200
            else:
                r = requests.get(url, headers=authorization.get_token_headers(), timeout=10)
                r.raise_for_status()
                return jsonify(r.json()), 200
        except ConnectionError as e:
            return {"Failed": "Couldn't established connection with 42 API."}, 500
        except requests.HTTPError as e:
            return {"Failed": "Couldn't get data from 42 API."}, 400
        except requests.Timeout as e:
            return {"Failed": "Timeout."}, 429
        except requests.TooManyRedirects as e:
            return {"Failed": "Exceed limit of redirects."}, 502
    else:
        return {"Failed": "You need provide a valid authorization code."}, 401
