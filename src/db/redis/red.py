from redis import StrictRedis, ConnectionError

from urllib.parse import urlparse
import os

from constants import REDISCLOUD_URL

def get_connection() -> StrictRedis:
    if REDISCLOUD_URL:
        url = urlparse(REDISCLOUD_URL)
        return StrictRedis(host=url.hostname, port=url.port, password=url.password, encoding="utf-8", decode_responses=True) 
    return StrictRedis(host='localhost', port=6379, db=1, encoding="utf-8", decode_responses=True)

def test_connection(conn: StrictRedis) -> None:
    try:
        conn.ping()
    except ConnectionError as e:
        raise

def set_token(conn: StrictRedis, token_id:str, token: str) -> None:
    conn.set(f"token_{token_id}", token, 7200)

def get_token(conn: StrictRedis, token_id: str) -> str:
    return conn.get(f"token_{token_id}")

def incr_next(conn: StrictRedis) -> None:
    conn.incr('next')

def set_next(conn: StrictRedis, next: int) -> None:
    conn.set('next', next)

def get_next(conn: StrictRedis) -> int:
    return conn.get('next')

if __name__ == '__main__':
    conn = get_connection()
    test_connection(conn)
