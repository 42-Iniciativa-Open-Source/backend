import pytest

import sys
sys.path.insert(1, '../')

from constants import AUTHORIZATION_CODE
import app as Client

#def test_home_page(client):
#    response = client.get('/')
#    assert response.status_code == 401

def test_slash(client):
    """ / endpoint """

    r = client.get('/')
    assert r.status_code == 401

def test_slash_authorized(client):
    """ / endpoint authorized """

    r = client.get('/', headers=dict(authorization=AUTHORIZATION_CODE))
    assert r.status_code == 200

@pytest.fixture
def client():
    Client.app.config['TESTING'] = True
    with Client.app.test_client() as client:
        yield client
