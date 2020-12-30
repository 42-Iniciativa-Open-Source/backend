from urllib.parse import urlsplit, parse_qs

def get_pages(headers: dict) -> dict:
    pages = {}
    links = headers["Link"].split(", ")
    for link in links:
        url = link.split(";")[0][1:-1]
        query_string = parse_qs(urlsplit(url).query)
        page = query_string["page"][0]
        if "last" in link:
            pages["last"] = page
        elif "next" in link:
            pages["next"] = page
    return pages
