from flask import Blueprint, request, jsonify, g
import requests, json

from utils import parser, fast_requests
from constants import AUTHORIZATION_CODE, INTRA_API_URL, APPS, ALLOWED_PAGINATED_ALL
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
            g.request = r
            if page and path in ALLOWED_PAGINATED_ALL and "all" in page:
                pages = parser.headers.get_pages(r.headers)
                url = parser.url.Url(url)
                urls = url.get_all_pages(pages, fast=True)
                data, headers = fast_requests.get.data(urls, path)
                g.headers = headers
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

@bp.after_request
def apply_caching(response):
    r = g.get("request")
    headers = g.get("headers")
    pages = parser.headers.get_pages(r.headers)
    for name, page in pages.items():
        response.headers[f"X-Page-{name.title()}"] = page
    response.headers["X-Application-Name"] = ', '.join(set(headers["X-Application-Name"])) or r.headers["X-Application-Name"]
    response.headers["X-Application-Id"] = r.headers["X-Application-Id"]
    response.headers["X-Application-Roles"] = r.headers["X-Application-Roles"]
    response.headers["X-Per-Page"] = r.headers["X-Per-Page"]
    response.headers["X-Total"] = r.headers["X-Total"]
    response.headers["X-Hourly-RateLimit-Limit"] = int(APPS) * 1200
    response.headers["X-Secondly-RateLimit-Limit"] = int(APPS) * 2
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
