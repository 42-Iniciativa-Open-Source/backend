from redis import StrictRedis, ConnectionError

def get_connection() -> StrictRedis:
    return StrictRedis(host='localhost', port=6379, db=1, charset="utf-8", decode_responses=True)

def test_connection(conn: StrictRedis) -> None:
    try:
        conn.ping()
    except ConnectionError as e:
        raise

if __name__ == '__main__':
    conn = get_connection()
    test_connection(conn)
