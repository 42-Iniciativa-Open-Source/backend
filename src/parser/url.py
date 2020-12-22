from urllib.parse import urlparse, parse_qsl, ParseResult, urlencode

def set_query_string(url: str, queries: dict) -> str:
    u = urlparse(url)
    query_string = dict(parse_qsl(u.query))
    for query in queries.items(): 
        query_string[query[0]] = query[1]
    res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(query_string), fragment=u.fragment)
    return res.geturl()
