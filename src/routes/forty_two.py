from flask import Blueprint, request, jsonify, g
import requests

from utils import parser, fast_requests
import constants as csts
import authorization

bp = Blueprint('forty_two', __name__, url_prefix='/42')

s = requests.Session()


@bp.route('/<path:path>', methods=['GET'])
def forty_two(path: str):
    header_authorization_code = request.headers.get("Authorization")
    if csts.AUTHORIZATION_CODE == header_authorization_code:
        url = f"{csts.INTRA_API_URL}/v2/{path}?{request.query_string.decode()}"
        page = request.args.get("page")
        try:
            r = s.get(url, headers=authorization.get_token_headers())
            g.request = r
            r.raise_for_status()
            if page and path in csts.ALLOWED_PAGINATED_ALL and "all" in page:
                pages = parser.headers.get_pages(r.headers)
                url = parser.url.Url(url)
                urls = url.get_all_pages(pages, fast=True)
                data, headers = fast_requests.get.data(urls, path)
                g.headers = headers
                return jsonify(data), 200
            else:
                return jsonify(r.json()), 200
        except ConnectionError:
            return {}, 500
        except requests.HTTPError:
            if r.headers["Content-Type"] == "application/json":
                return jsonify(r.json()), r.status_code
            return {}, r.status_code
        except requests.Timeout:
            return {}, 429
        except requests.TooManyRedirects:
            return {}, 502
    else:
        return {"Failed": "You need provide a valid authorization code."}, 401


@bp.after_request
def apply_caching(response):
    r = g.get("request")
    headers = g.get("headers")
    try:
        if headers:
            response.headers["X-App-Name"] = ', '.join(
                set(headers["X-Application-Name"])
            )
        else:
            response.headers["X-App-Name"] = r.headers["X-Application-Name"]
            pages = parser.headers.get_pages(r.headers)
            for name, page in pages.items():
                response.headers[f"X-Page-{name.title()}"] = page
        response.headers["X-App-Id"] = r.headers["X-Application-Id"]
        response.headers["X-App-Roles"] = r.headers["X-Application-Roles"]
        response.headers["X-Hourly-RateLimit-Limit"] = int(csts.APPS) * 1200
        response.headers["X-Secondly-RateLimit-Limit"] = int(csts.APPS) * 2
        response.headers["X-Per-Page"] = r.headers["X-Per-Page"]
        response.headers["X-Total"] = r.headers["X-Total"]
    except (AttributeError, KeyError):
        pass
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
