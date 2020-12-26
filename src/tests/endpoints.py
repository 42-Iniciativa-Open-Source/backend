import requests, json

from functools import reduce

r = requests.get("https://api.intra.42.fr/apidoc")
docs = json.loads(r.text)

def fill_ids(endpoints: list) -> list:
    filled_endpoints = []
    for endpoint in endpoints:
      if ':' in endpoint:
        replaces = (":user_id", "66504"), (":id", "9"), (":cursus_id", "21"), (":campus_id", "20"), (":project_id", "1874"), (":project_sessions_id", "5249"), (":achievement_id", "1"), (":bloc_id", "1"), (":close_id", "1"), (":team_id", "31"), (":event_id", "5376"), (":tag_id", "1"), (":project_session_id", "5249"), (":skill_id", "1"), (":role_id", "1"), (":notion_id", "1"), (":partnership_id", "563"), (":issue_id", "1"), (":quest_id", "1"), (":title_id", "27"), (":coalition_id", "1"), (":product_id", "1"), (":dash_id", "1"), (":group_id", "1"), (":expertise_id", "1"), (":accreditation_id", "1"), (":scale_team_id", "1"), (":field", "created_at"), (":interval", "day")
        filled_endpoints.append(reduce(lambda a, kv: a.replace(*kv), replaces, endpoint))
        continue
      filled_endpoints.append(endpoint)
    return filled_endpoints

def get_allowed_endpoints() -> list:
    all_42_endpoints = docs["docs"]["resources"]
    endpoints_allowed = []

    for endpoint in all_42_endpoints.values():
      for methods in endpoint["methods"]:
        if not methods["metadata"] or not methods["metadata"].get("roles"):
          for url in methods["apis"]:
            if url["http_method"] == "GET":
                endpoints_allowed.append(url["api_url"][4:])
    
    return fill_ids(endpoints_allowed)

def get_paginated_endpoints() -> list:
    all_42_endpoints = docs["docs"]["resources"]
    endpoints_paginated = []

    for endpoint in all_42_endpoints.values():
        for methods in endpoint["methods"]:
            if methods["metadata"] and not methods["metadata"].get("roles") and methods["metadata"].get("paginated"):
                for url in methods["apis"]:
                    if url["http_method"] == "GET":
                        endpoints_paginated.append(url["api_url"][4:])

    return fill_ids(endpoints_paginated) 
