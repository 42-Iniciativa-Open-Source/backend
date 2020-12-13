from redis import StrictRedis, ConnectionError
from urllib.parse import urlparse
import os

def get_connection() -> StrictRedis:
    redis_cloud_url = os.environ.get('REDISCLOUD_URL')
    if redis_cloud_url:
        url = urlparse(redis_cloud_url)
        return StrictRedis(host=url.hostname, port=url.port, password=url.password, charset="utf-8", decode_responses=True) 
    return StrictRedis(host='localhost', port=6379, db=1, charset="utf-8", decode_responses=True)

def test_connection(conn: StrictRedis) -> None:
    try:
        conn.ping()
    except ConnectionError as e:
        raise

def set_token(conn: StrictRedis, token: str) -> None:
    conn.set('token', token, 7200)

def get_token(conn: StrictRedis) -> str:
    return conn.get('token')

if __name__ == '__main__':
    conn = get_connection()
    test_connection(conn)
