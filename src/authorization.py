import requests, json
from datetime import datetime

import constants
from db import red

red_conn = red.get_connection()

def create_token():
    """Generate token and store on database"""
    data = {
        "grant_type": "client_credentials",
        "client_id": constants.CLIENT_ID,
        "client_secret": constants.CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        r = requests.post(f"{constants.INTRA_API_URL}/oauth/token", headers=headers, data=data)
    except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
        raise Exception("Connection to generate token with API failed for some reason.")
    if r.status_code == requests.codes.ok:
        r = json.loads(r.text)
        red.set_token(red_conn, r["access_token"])
    return r["access_token"]

def get_token():
    """Get current valid token"""
    token = red.get_token(red_conn)
    if not token:
        token = create_token()
    return token 

def get_token_headers():
    """Return header with token"""
    return {"Authorization": f"Bearer {get_token()}"}
