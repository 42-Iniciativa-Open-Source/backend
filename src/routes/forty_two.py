from flask import Blueprint, request, jsonify
import requests, json

from constants import AUTHORIZATION_CODE, INTRA_API_URL
import authorization

bp = Blueprint('forty_two', __name__, url_prefix='/42')

@bp.route('/<path:path>', methods=['GET'])
def forty_two(path: str):
    header_authorization_code = request.headers.get("Authorization")
    if AUTHORIZATION_CODE == header_authorization_code:
        url = f"{INTRA_API_URL}/v2/{path}?{request.query_string.decode()}"
        try:
            r = requests.get(url, headers=authorization.get_token_headers(), timeout=10)
            r.raise_for_status()
        except ConnectionError as e:
            return {"Failed": "Couldn't established connection with 42 API."}, 500
        except requests.HTTPError as e:
            return {"Failed": "Couldn't get data from 42 API."}, 400
        except requests.Timeout as e:
            return {"Failed": "Timeout."}, 429
        except requests.TooManyRedirects as e:
            return {"Failed": "Exceed limit of redirects."}, 502
        return jsonify(r.json()), 200
    else:
        return {"Failed": "You need provide a valid authorization code."}, 401
