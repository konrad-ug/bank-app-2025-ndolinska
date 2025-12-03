import pytest
import requests

base_url = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture
def acc():
    return {
        "first_name": "Jan",
        "last_name": "Testowy",
        "pesel": "12345678901"
    }

def test_create(acc):
    response = requests.post(base_url, json=acc)  
    assert response.status_code == 201
    assert response.json() == {"message": "Account created"}
def test_find(acc):
    response = requests.get(f"{base_url}/{acc["pesel"]}")  
    assert response.status_code == 200
    data = response.json()
    assert data["pesel"] == acc["pesel"]
    assert data["first_name"] == acc["first_name"]
    assert data["last_name"] == acc["last_name"]

def test_update(acc):
    new= {"last_name":"Nowotestowy"}
    response = requests.patch(f"{base_url}/{acc["pesel"]}", json=new)
    assert response.status_code == 200
    get_response = requests.get(f"{base_url}/{acc["pesel"]}")
    assert get_response.json()["last_name"] == new["last_name"]
def test_delete(acc):
    delete_response = requests.delete(f"{base_url}/{acc["pesel"]}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Account deleted"}
def test_find_nonexistant(acc):
    response = requests.get(f"{base_url}/{acc["pesel"]}")
    assert response.status_code == 404
    assert response.json() == {"message": "Account not found"}


