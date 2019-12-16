import requests
import pytest


@pytest.fixture(scope='module')
def create_delete_user(request):
    payload = {
        'username': 'testuser',
        'first_name': 'test',
        'last_name': 'user',
        'email': 'test@example.com',
        'password': 'example'
    }
    r = requests.post('http://localhost:5000/users', json=payload)
    assert r.status_code == 201

    def fin():
        r = requests.delete('http://localhost:5000/users/testuser')
        assert r.status_code == 200

    request.addfinalizer(fin)

    return


def test_user_get(create_delete_user):
    r = requests.get('http://localhost:5000/users')
    response = r.json()
    assert response[0]['username'] == 'testuser'
    assert type(response) is list
    assert r.status_code == 200


def test_user_put(create_delete_user):
    r = requests.get('http://localhost:5000/users/testuser')
    assert r.status_code == 200
    response = r.json()
    response.pop('created_at')
    response.pop('id')
    test = {
        'username': 'testuser',
        'first_name': 'test',
        'last_name': 'user',
        'email': 'test@example.com',
        'password': 'example'
    }
    for key in response:
        assert key in test
        assert response[key] == test[key]

    payload = {
        'first_name': 'test_update'
    }
    r = requests.put('http://localhost:5000/users/testuser', json=payload)
    assert r.status_code == 200

    r = requests.get('http://localhost:5000/users/testuser')
    assert r.status_code == 200
    response = r.json()
    response.pop('created_at')
    response.pop('id')
    test = {
        'username': 'testuser',
        'first_name': 'test_update',
        'last_name': 'user',
        'email': 'test@example.com',
        'password': 'example'
    }
    for key in response:
        assert key in test
        assert response[key] == test[key]
