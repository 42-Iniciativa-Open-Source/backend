from urllib.parse import urlparse, parse_qsl, ParseResult, urlencode
import requests

import authorization
from utils import parser

class Url:
    def __init__(self, url):
        self.url = url
        self.url_parse = urlparse(url)
        self.url_qs = dict(parse_qsl(self.url_parse.query))
    
    def rename_qs(self, queries):
        u = self.url_parse
        for key, value in queries.items():
            self.url_qs[value] = self.url_qs.pop(key)
        return ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(self.url_qs), fragment=u.fragment).geturl()
    
    def set_qs(self, queries):
        u = self.url_parse
        for key, value in queries.items():
            self.url_qs[key] = value
        return ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(self.url_qs), fragment=u.fragment).geturl()
   
    def get_all_pages(self, pages, fast):
        urls = []
        if fast:
            self.url = self.rename_qs({"page": "page[number]"})
            self.url = self.set_qs({"page[number]": 1, "page[size]": 100})
            r = requests.get(self.url, headers=authorization.get_token_headers())
            pages = parser.headers.get_pages(r.headers)
        for page in range(1, int(pages["last"]) + 1):
            url = self.set_qs({"page[number]": page})
            urls.append(url)
        return urls
