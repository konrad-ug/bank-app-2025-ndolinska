from src.personal_account import Personal_Account
from src.company_account import Company_Account
from src.account import Account
import pytest # pyright: ignore[reportMissingImports]

#Zmieniono tutaj zwykłe testy na fixtures
#====================TESTY PODSTAWOWYCH PRZELEWÓW ===============================
class TestTransfers:
    @pytest.fixture()
    def acc(self):
        acc = Account()
        return acc
    @pytest.mark.parametrize("balance, amount_in, amount_out, expected_balance",[
        (0.0,200.0,0.0,200.0),
        (0.0,"przelew",0.0,0.0),
        (0.0,-50.0,0.0,0.0),
        (0.0,55.0,50.0,5.0),
        (0.0,0.0,"przelew",0.0),
        (0.0,0.0,-10.0,0.0),
        (0.0,0.0,10.0,0.0)
        ],ids=[
            "incoming success",
            "incoming not a number",
            "incoming a negative amount",
            "outgoing success",
            "outgoing not a number",
            "outgoing a negative amount",
            "outgoing not enough balance"
        ])
    def test_incoming_outgoing(self, acc, balance, amount_in, amount_out, expected_balance):
        acc.balance = balance
        acc.transfer_incoming(amount_in)
        acc.transfer_outgoing(amount_out)
        assert acc.balance == expected_balance

#====================TESTY PRZELEWÓW EKSPRESOWYCH ===============================
class TestExpressTransferPersonal:
# PRZELEWY Z KONTA OSOBISTEGO
   @pytest.fixture()
   def acc(self):
        acc = Personal_Account("John", "Doe", "5443222277")
        return acc
   @pytest.mark.parametrize("balance, amount_in, amount_out, expected_balance",[
       (0.0,100.0,40.0,59.0),
       (0.0,30.0,40.0,30.0),
       (0.0,30.0,30.0,-1.0)
   ],ids=[
   "express_success",
   "not enough balance",
   "test fee debit"])
   def test_express_personal(self,acc,balance,amount_in,amount_out,expected_balance):
       acc.balance = balance
       acc.transfer_incoming(amount_in)
       acc.transfer_express_outgoing(amount_out)
       assert acc.balance == expected_balance
# PRZELEWY Z KONTA FIRMOWEGO
class TestExpressCompany:
   @pytest.fixture()
   def acc(self):
        acc = Company_Account("ABC", "544322277")
        return acc
   @pytest.mark.parametrize("balance, amount_in, amount_out, expected_balance",[
       (0.0,100.0,40.0,55.0),
       (0.0,30.0,40.0,30.0),
       (0.0,30.0,30.0,-5.0)
   ],ids=[
   "express_success",
   "not enough balance",
   "test fee debit"])
   def test_express_personal(self,acc,balance,amount_in,amount_out,expected_balance):
       acc.balance = balance
       acc.transfer_incoming(amount_in)
       acc.transfer_express_outgoing(amount_out)
       assert acc.balance == expected_balance

