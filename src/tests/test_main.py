import pytest

import sys
sys.path.insert(1, '../')

from endpoints import get_allowed_endpoints, get_paginated_endpoints
from constants import AUTHORIZATION_CODE
import app as Client

endpoints_allowed = get_allowed_endpoints()
endpoints_paginated = get_paginated_endpoints()

def test_slash(client):
    """ / endpoint """

    r = client.get('/')
    assert r.status_code == 401

def test_slash_authorized(client):
    """ / endpoint authorized """

    r = client.get('/', headers=dict(authorization=AUTHORIZATION_CODE))
    assert r.status_code == 200

@pytest.mark.parametrize('endpoint', endpoints_allowed)
def test_allowed_endpoints(client, endpoint):
    """ all allowed endpoints available on https://api.intra.42.fr/apidoc """
    r = client.get(f"/42/{endpoint}", headers=dict(authorization=AUTHORIZATION_CODE))
    assert r.status_code in (200, 0)

@pytest.mark.parametrize('endpoint', endpoints_paginated)
def test_paginated_endpoints(client, endpoint):
    """ all paginated endpoints available on https://api.intra.42.fr/apidoc """
    r = client.get(f"/42/{endpoint}?page=all", headers=dict(authorization=AUTHORIZATION_CODE))
    assert r.status_code == 200

@pytest.fixture
def client():
    Client.app.config['TESTING'] = True
    with Client.app.test_client() as client:
        yield client
