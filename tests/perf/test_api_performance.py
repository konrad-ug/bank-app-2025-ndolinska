import pytest
import requests
url="http://127.0.0.1:5000"
class TestPerformance:
    def test_perf_create_delete_account_loop(self):
        for i in range(100):
            account = {
                 "first_name": "Konto",
                 "last_name": f"{i}",
                 "pesel": "12345678902"}
            try:
                response = requests.post(f"{url}/api/accounts", json=account, timeout=0.5)
                assert response.status_code in [200,201]
                del_resp = requests.delete(f"{url}/api/accounts/{account['pesel']}", timeout=0.5)
                assert del_resp.status_code in [200, 204], f"Delete failed at {i} try"
            except requests.exceptions.Timeout:
                pytest.fail(f"Performance check failed! Request took longer than 0.5s at iteration {i}")

    def test_perf_incoming_transfers_loop(self):
        account = {
                 "first_name": "Konto",
                 "last_name": "Testowe",
                 "pesel": "12345678902"}
        create_resp = requests.post(f"{url}/api/accounts", json=account)
        assert create_resp.status_code in [200, 201]
        transfer_amount = 10
        for i in range(100):
            transfer = {"amount": transfer_amount, "type": "incoming"}
            try:
                resp = requests.post(
                    f"{url}/api/accounts/{account['pesel']}/transfer", 
                    json=transfer, 
                    timeout=0.5
                )
            except requests.exceptions.Timeout:
                pytest.fail(f"Performance check failed! Transfer took longer than 0.5s at iteration {i}")
        get_resp = requests.get(f"{url}/api/accounts/{account['pesel']}")
        assert get_resp.status_code == 200
        final_balance = get_resp.json()['balance']
        expected_balance = 100 * transfer_amount
        assert final_balance == expected_balance, f"Balance check failed! Expected {expected_balance}, got {final_balance}"
        delete_response= requests.delete(f"{url}/api/accounts/{account['pesel']}")
        assert delete_response.status_code  == 200