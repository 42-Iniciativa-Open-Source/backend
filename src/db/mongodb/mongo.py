from pymongo import MongoClient

from constants import MONGODB_CONN_STR

def get_connection() -> MongoClient:
    return MongoClient(MONGODB_CONN_STR)

def test_connection(conn: MongoClient) -> None:
    try:
        conn.server_info()
    except ConnectionError as e:
        raise

if __name__ == '__main__':
    conn = get_connection()
    test_connection(conn)
