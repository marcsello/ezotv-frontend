import pytest

import ezotv


@pytest.fixture
def client():
    ezotv.app.config['TESTING'] = True

    with ezotv.app.test_client() as client:
        yield client


def test_access_denied(client):

    r = client.get('/api/user')

    assert r.status_code == 401


def test_access_denied2(client):

    r = client.get('/api/user', headers={"Authorization": "invalidkey"})

    assert r.status_code == 401


def test_empty_database(client):

    r = client.get('/api/user', headers={"Authorization": "testkey"})

    assert len(r.json) == 0




