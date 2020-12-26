import requests, json
from requests.exceptions import HTTPError, Timeout, TooManyRedirects
from datetime import datetime

from constants import INTRA_API_URL, SECRETS, APPS
from db.redis import red

red_conn = red.get_connection()

def create_token(token_id: int) -> str:
    """Generate token and store on database"""
    data = {
        "grant_type": "client_credentials",
        "client_id": SECRETS[f"APP_{token_id}"]["CLIENT_ID"],
        "client_secret": SECRETS[f"APP_{token_id}"]["CLIENT_SECRET"]
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        r = requests.post(f"{INTRA_API_URL}/oauth/token", headers=headers, data=data)
    except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
        raise Exception("Connection to generate token with API failed for some reason.")
    if r.status_code == requests.codes.ok:
        r = json.loads(r.text)
        red.set_token(red_conn, token_id, r["access_token"])
    return r["access_token"]

def get_token() -> str:
    """Get current valid token"""
    next = red.get_next(red_conn)
    if not next or int(next) >= int(APPS) + 1:
        red.set_next(red_conn, 2)
        next = 1
    else:
        red.incr_next(red_conn)
    token = red.get_token(red_conn, next)
    if not token:
        token = create_token(next)
    return token 

def get_token_headers() -> dict:
    """Return header with token"""
    return {"Authorization": f"Bearer {get_token()}"}
