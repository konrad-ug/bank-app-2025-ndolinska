import pytest
import requests

class TestTransfers:
    url="http://127.0.0.1:5000"
    account = {
        "first_name": "Jan",
        "last_name": "Testowy",
        "pesel": "12345678902"
    }
    trans_inc = {
        "amount":1000,
        "type": "incoming"
    }
    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        response = requests.post(f"{self.url}/api/accounts",json=self.account)
        assert response.status_code == 201
        pesel = self.account['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=self.trans_inc)
        assert response.status_code == 200
        yield
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account['pesel']
            requests.delete(f"{self.url}/api/accounts/{pesel}")

    def test_incoming_transfers(self):
        transfer_data ={
            "amount": 500,
            "type": "incoming"
        }
        pesel = self.account['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 200
        data =response.json()
        assert data['message'] == "Transfer successful"
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        account_data = response.json()
        assert account_data['balance'] == self.trans_inc['amount'] + transfer_data['amount']
    def test_outgoing_success(self):
        transfer_data ={
            "amount": 500,
            "type": "outgoing"
        }
        pesel = self.account['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 200
        data =response.json()
        assert data['message'] == "Transfer successful"
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        account_data = response.json()
        assert account_data['balance'] == self.trans_inc['amount'] - transfer_data['amount'] 
    def test_outgoing_insufficient_funds(self):
        transfer_data ={
            "amount": 1500,
            "type": "outgoing"
        }
        pesel = self.account['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 422
        data =response.json()
        assert data['message'] == "There was an issue with transfer"
    def test_express(self):
        transfer_data ={
            "amount": 500,
            "type": "express"
        }
        pesel = self.account['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 200
        data =response.json()
        assert data['message'] == "Transfer successful"
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        account_data = response.json()
        assert account_data['balance'] == self.trans_inc['amount'] - transfer_data['amount'] - 1
    def test_express_debit(self):
        transfer_data ={
            "amount": 1000,
            "type": "express"
        }
        pesel = self.account['pesel']
        response = requests.post(f"{self.url}/api/accounts/{pesel}/transfer", json=transfer_data)
        assert response.status_code == 200
        data =response.json()
        assert data['message'] == "Transfer successful"
        response = requests.get(f"{self.url}/api/accounts/{pesel}")
        assert response.status_code == 200
        account_data = response.json()
        assert account_data['balance'] == -1