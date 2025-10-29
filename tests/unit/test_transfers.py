from src.personal_account import Personal_Account
from src.company_account import Company_Account
from src.account import Account
#====================TESTY PODSTAWOWYCH PRZELEWÓW ===============================
class TestTransfers:
    def test_transfer_incoming(self):
        account = Account()
        account.transfer_incoming(200)
        assert account.balance == 200.0

    def test_transfer_incoming_notnum(self):
        account =Account()
        account.transfer_incoming("przelew")
        assert account.balance == 0.0

    def test_transfer_incoming_negative(self):
        account = Account()
        account.transfer_incoming(-50.0)
        assert account.balance == 0.0

    def test_transfer_outgoing(self):
        account = Account()
        account.transfer_incoming(50.0)
        account.transfer_outgoing(50.0)
        assert account.balance == 0.0

    def test_transfer_outgoing_negative(self):
        account = Account()
        account.transfer_outgoing(-60)
        assert account.balance == 0.0
    
    def test_transfer_outgoing_notnum(self):
        account = Account()
        account.transfer_outgoing("przelew")
        assert account.balance == 0.0
    
    def test_transfer_outgoing_not_enough_balance(self):
        account = Account()
        account.transfer_outgoing(60.0)
        assert account.balance == 0.0

    def test_both_transfers(self):
        account = Account()
        account.transfer_incoming(200)
        account.transfer_outgoing(50)
        assert account.balance == 150.0
  
#====================TESTY PRZELEWÓW EKSPRESOWYCH ===============================
class TestExpressTransfer:
# PRZELEWY Z KONTA OSOBISTEGO
    def test_personal_account_transfer_express(self):
        acc = Personal_Account("John", "Doe", "5443222277")
        acc.transfer_incoming(100.0)
        acc.transfer_express_outgoing(40.0)
        assert acc.balance == 59.0

    def test_personal_account_transfer_express_not_enough_balance(self):
        acc = Personal_Account("John", "Doe", "5443222277")
        acc.transfer_incoming(30.0)
        acc.transfer_express_outgoing(40.0)
        assert acc.balance == 30.0

    def test_personal_account_transfer_express_fee_debit(self):
        acc = Personal_Account("John", "Doe", "5443222277")
        acc.transfer_incoming(30.0)
        acc.transfer_express_outgoing(30.0)
        assert acc.balance == -1.0
        
# PRZELEWY Z KONTA FIRMOWEGO
    def test_company_account_transfer_express(self):
        acc = Company_Account("ABC","544322227")
        acc.transfer_incoming(100.0)
        acc.transfer_express_outgoing(40.0)
        assert acc.balance == 55.0

    def test_company_account_transfer_express_not_enough_balance(self):
        acc = Company_Account("ABC", "544322227")
        acc.transfer_incoming(30.0)
        acc.transfer_express_outgoing(36.0)
        assert acc.balance == 30.0

    def test_company_account_transfer_express_fee_debit(self):
        acc = Company_Account("ABC", "544322227")
        acc.transfer_incoming(30.0)
        acc.transfer_express_outgoing(30.0)
        assert acc.balance == -5.0

