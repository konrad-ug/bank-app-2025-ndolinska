import pytest
from app.api import app, registry

base_url = '/api/accounts'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        registry.accounts = []

@pytest.fixture
def acc():
    return {
        "first_name": "Jan",
        "last_name": "Testowy",
        "pesel": "12345678901"
    }
@pytest.fixture(autouse=True)
def clean_registry():
    registry.accounts = []

def test_create(client, acc):
        response = client.post(base_url, json=acc)  
        assert response.status_code == 201
        assert response.json['message'] ==  "Account created"
        assert registry.return_length() == 1

def test_create_failure(client, acc):
        response = client.post(base_url, json=acc)  
        assert response.status_code == 201
        assert response.json['message'] ==  "Account created"
        assert registry.return_length() == 1
        response = client.post(base_url, json=acc)  
        assert response.status_code == 409
        assert response.json['message'] ==  "Account with this pesel already exists"

def test_find(client, acc):
        client.post(base_url, json=acc)  
        response = client.get(f"{base_url}/{acc['pesel']}")  
        assert response.status_code == 200
        assert response.json['pesel'] == acc['pesel']
    
def test_update(client, acc):
        client.post(base_url, json=acc)
        new= {"last_name":"Nowotestowy"}
        response =  client.patch(f"{base_url}/{acc['pesel']}", json=new)
        assert response.status_code == 200
        get_response = client.get(f"{base_url}/{acc['pesel']}")
        assert get_response.json['last_name'] == new['last_name']

def test_delete(client, acc):
        client.post(base_url, json=acc)
        delete_response = client.delete(f"{base_url}/{acc['pesel']}")
        assert delete_response.status_code == 200
        assert delete_response.json['message'] ==  "Account deleted"
def test_find_nonexistant(client, acc):
        response = client.get(f"{base_url}/{acc['pesel']}")
        assert response.status_code == 404
        assert response.json['message'] ==  "Account not found"
