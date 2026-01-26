import pytest
from src.personal_account import Personal_Account
from src.mongo_accounts_repository import MongoAccountsRepository

@pytest.fixture
def sample_account():
    acc = Personal_Account("Jan", "Kowalski", "90010112345")
    acc.balance = 100.0
    acc.history = [10.0, -5.0]
    return acc

def test_save_all_clears_collection_and_saves_accounts(mocker, sample_account):
    mock_collection = mocker.Mock()
    repo = MongoAccountsRepository(collection=mock_collection)
    
    accounts = [sample_account]
    repo.save_all(accounts)
    mock_collection.delete_many.assert_called_once_with({})
    mock_collection.update_one.assert_called_once()
    call_args = mock_collection.update_one.call_args
    filter_query = call_args[0][0]
    update_doc = call_args[0][1]
    kwargs = call_args[1]

    assert filter_query == {"pesel": "90010112345"}
    assert update_doc["$set"]["first_name"] == "Jan"
    assert update_doc["$set"]["balance"] == 100.0
    assert update_doc["$set"]["history"] == [10.0, -5.0]
    assert kwargs['upsert'] is True

def test_load_all_returns_account_objects(mocker):
    mock_collection = mocker.Mock()
    repo = MongoAccountsRepository(collection=mock_collection)

    db_doc = {
        "first_name": "Anna",
        "last_name": "Nowak",
        "pesel": "80010112345",
        "balance": 250.0,
        "history": [50.0]
    }
    
    mock_collection.find.return_value = [db_doc]
    loaded_accounts = repo.load_all()
    assert len(loaded_accounts) == 1
    assert isinstance(loaded_accounts[0], Personal_Account)
    assert loaded_accounts[0].first_name == "Anna"
    assert loaded_accounts[0].pesel == "80010112345"
    assert loaded_accounts[0].balance == 250.0
    assert loaded_accounts[0].history == [50.0]

def test_init_creates_client_when_no_collection_provided(mocker):
    mock_mongo_cls = mocker.patch("src.mongo_accounts_repository.MongoClient")
    mock_client_instance = mock_mongo_cls.return_value
    
    mock_db = mocker.Mock(name="mock_db")
    expected_collection = mocker.Mock(name="mock_collection")
    mock_client_instance.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = expected_collection
    repo = MongoAccountsRepository()
    assert repo._collection == expected_collection
    mock_mongo_cls.assert_called_once()

def test_load_all_using_mocker_style(mocker):
    mock_collection = mocker.Mock()
    
    doc1 = {"first_name": "Jan", "last_name": "Kowalski", "pesel": "90010112345", "balance": 100.0, "history": []}
    doc2 = {"first_name": "Anna", "last_name": "Nowak", "pesel": "80010154321", "balance": 200.0, "history": []}
    
    mock_collection.find.return_value = [doc1, doc2]

    repo = MongoAccountsRepository(collection=mock_collection)

    result = repo.load_all()

    assert len(result) == 2
    assert result[0].first_name == "Jan"
    assert result[1].first_name == "Anna"
    mock_collection.find.assert_called_once()

