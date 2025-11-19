from src.personal_account import Personal_Account
import pytest # pyright: ignore[reportMissingImports]
class Test_Submit_For_Loan():
 
    @pytest.fixture()
    def acc(self):
        acc = Personal_Account("John", "Doe", "5443222277")
        return acc
    @pytest.mark.parametrize("history, amount, expected_result, expected_balance",[
        ([1.0,-1.0,-1.0,1.0,1.0,5000.0], 4000.0, True, 4000.0),
        ([5000.0,2000.0,30.0,30.0],1.0,False,0.0),
        ([1.0,1.0,1.0,1.0,1.0],10.0,False,0.0),
        ([500.0,500.0,500.0,-300.0,-1.0,500.0],1000.0,False,0.0)],ids=[
            "success",
            "not enough transactions",
            "sum too little",
            "last three are not incoming"
        ])
    def test_loan(self, acc, history, amount, expected_result, expected_balance):
        acc.history = history
        result = acc.submit_for_loan(amount)
        assert result == expected_result
        assert acc.balance == expected_balance

    # def test_success(self,acc):
    #     acc.history = [1.0,-1.0,-1.0,1.0,1.0,5000.0]
    #     result = acc.submit_for_loan(4000.0)
    #     assert acc.balance == 4000.0
    #     assert result 

    # def test_not_enough_transactions(self,acc):
    #     acc.transfer_incoming(5000.0)
    #     acc.transfer_incoming(2000.0)
    #     acc.transfer_incoming(30.0)
    #     acc.transfer_incoming(30.0)
    #     result = acc.submit_for_loan(1.0)
    #     assert acc.balance == 7060.0
    #     assert result == False

    # def test_sum_too_little(self,acc):
    #     acc.transfer_incoming(1.0)
    #     acc.transfer_incoming(1.0)
    #     acc.transfer_incoming(1.0)
    #     acc.transfer_incoming(1.0)
    #     acc.transfer_incoming(1.0)
    #     result = acc.submit_for_loan(10.0)
    #     assert acc.balance == 5.0
    #     assert result == False

    # def test_last_three_not_incoming(self,acc):
    #     acc.transfer_incoming(500.0)
    #     acc.transfer_incoming(500.0)
    #     acc.transfer_incoming(500.0)
    #     acc.transfer_express_outgoing(300.0)
    #     acc.transfer_incoming(500.0)
    #     result = acc.submit_for_loan(1000.0)
    #     assert acc.balance == 1699.0
    #     assert result == False
    