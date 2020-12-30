import os

INTRA_API_URL = "https://api.intra.42.fr"

MONGODB_CLUSTER = os.environ.get("MONGODB_CLUSTER")
MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
MONGODB_CONN_STR = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}.glyt0.mongodb.net"

#defined by heroku Redis integration
REDISCLOUD_URL = os.environ.get('REDISCLOUD_URL')

ALLOWED_PAGINATED_ALL = ("apps")

def get_secrets() -> dict:
    SECRETS = {}
    for app in range(1, int(APPS) + 1):
        client_id = os.environ.get(f"CLIENT_ID_42_{app}")
        client_secret = os.environ.get(f"CLIENT_SECRET_42_{app}")
        SECRETS[f"APP_{app}"] = {"CLIENT_ID": client_id, "CLIENT_SECRET": client_secret}
    return SECRETS

try:
    AUTHORIZATION_CODE = os.environ.get("AUTHORIZATION_CODE")
    APPS = os.environ.get("APPS")
    SECRETS = get_secrets()
except TypeError as e:
    print("You need set some environment variables to properly start the server.")
    quit()
