from src.company_account import Company_Account
import pytest # pyright: ignore[reportMissingImports]
class Test_Company_Loan():
 
    @pytest.fixture()
    def acc(self):
        acc = Company_Account("JANUSZEX", "1234567890")
        return acc
    @pytest.mark.parametrize("history, balance, amount, expected_result, expected_balance",[
        ([5000.0,-1775.0], 3225.0, 1000.0, True, 4225.0),
        ([5000.0,-1775.0,1775.0], 5000.0, 2501.0, False, 5000.0),
        ([5000.0],5000.0,2500.0,False,5000.0),
        ([5000.0,-1775.0,1775.0,-1775.0],3225.0,200.0,True,3425.0),
        ([5000.0,1775.0],6775.0,3000.0,False,6775.0)],ids=[
            "success",
            "balance too small",
            "no ZUS transfer",
            "more than one ZUS transfer",
            "check if works with positive"
        ])
    
    def test_loan(self, acc, balance, history, amount, expected_result, expected_balance):
        acc.history = history
        acc.balance = balance
        result = acc.take_loan(amount)
        assert result == expected_result
        assert acc.balance == expected_balance