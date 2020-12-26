from urllib.parse import urlparse, parse_qsl, ParseResult, urlencode
import requests

import authorization
from utils import parser

def rename_query_string(url: str, queries: dict) -> str:
    u = urlparse(url)
    query_string = dict(parse_qsl(u.query))
    for query in queries.items():
        query_string[query[1]] = query_string.pop(query[0])
    res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(query_string), fragment=u.fragment)
    return res.geturl()

def set_query_string(url: str, queries: dict) -> str:
    u = urlparse(url)
    query_string = dict(parse_qsl(u.query))
    for query in queries.items(): 
        query_string[query[0]] = query[1]
    res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(query_string), fragment=u.fragment)
    return res.geturl()

def all_pages(url: str, pages: dict, fast: bool=False) -> list:
    urls = []
    if fast:
        url = parser.url.rename_query_string(url, {"page": "page[number]"})
        url = parser.url.set_query_string(url, {"page[number]": 1, "page[size]": 100})
        r = requests.get(url, headers=authorization.get_token_headers())
        pages = parser.headers.get_pages(r.headers)
    for page in range(1, int(pages["last"]) + 1):
        url = parser.url.set_query_string(url, {"page[number]": page})
        urls.append(url)
    return urls
