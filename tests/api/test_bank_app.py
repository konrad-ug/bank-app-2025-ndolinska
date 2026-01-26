import pytest
import os
from pymongo import MongoClient
from app.api import app, registry
from src.personal_account import Personal_Account

os.environ["MONGO_DB"] = "test_bank_app"

@pytest.fixture(scope="function")
def client():
    registry.accounts = []
    
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function", autouse=True)
def clean_mongo():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    db_name = os.getenv("MONGO_DB", "test_bank_app")
    
    client[db_name]["accounts"].delete_many({})
    
    yield 

    client[db_name]["accounts"].delete_many({})
    client.close()

def test_full_save_load_scenario(client):

    pesel = "99010112345"
    create_data = {
        "first_name": "Integration",
        "last_name": "Test",
        "pesel": pesel
    }
    client.post("/api/accounts", json=create_data)
 
    assert registry.search_account(pesel) is not None

    save_resp = client.post("/api/accounts/save")
    assert save_resp.status_code == 200

    registry.accounts = []
    assert registry.search_account(pesel) is None # Pusto w pamięci

    load_resp = client.post("/api/accounts/load")
    assert load_resp.status_code == 200

    loaded_account = registry.search_account(pesel)
    assert loaded_account is not None
    assert loaded_account.first_name == "Integration"
    assert loaded_account.balance == 0.0 

def test_data_is_actually_in_mongodb(client):
   
    pesel = "88010154321"
    acc = Personal_Account("Real", "Database", pesel)
    acc.balance = 123.0
    registry.add_account(acc)

    client.post("/api/accounts/save")

    mongo_client = MongoClient("mongodb://localhost:27017")
    db = mongo_client["test_bank_app"]
    collection = db["accounts"]
    
    doc = collection.find_one({"pesel": pesel})
    
    assert doc is not None
    assert doc["first_name"] == "Real"
    assert doc["balance"] == 123.0
    
    mongo_client.close()