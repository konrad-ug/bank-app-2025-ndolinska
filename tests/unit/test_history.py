from src.personal_account import Personal_Account
from src.company_account import Company_Account
from src.account import Account
#TEST ZWYKLYCH PRZELEWOW
class TestHistory:
    def test_transaction_incoming(self):
        account = Account()
        account.transfer_incoming(200)
        assert account.balance == 200.0
        assert account.history == [200.0]
    def test_transaction_incoming_outgoing(self):
        account = Account()
        account.transfer_incoming(200)
        account.transfer_outgoing(200)
        assert account.balance == 0.0
        assert account.history == [200.0,-200.0]
#TEST PRZELEWÓW EKSPRESOWYCH (KONTA OSOBISTE)
class TestExpressHistoryPersonal:
     def test_express_outgoing(self):
        account = Personal_Account("Ola", "Kowal", "1234567891")
        account.transfer_incoming(200)
        account.transfer_express_outgoing(200)
        assert account.balance == -1.0
        assert account.history == [200.0,-200.0,-1.0]
#TEST PRZELEWÓW EKSPRESOWYCH (KONTA FIRMOWE)
class TestExpressHistoryCompany:
     def test_express_outgoing(self):
        account = Company_Account("ABC","544322227")
        account.transfer_incoming(200)
        account.transfer_express_outgoing(200)
        assert account.balance == -5.0
        assert account.history == [200.0,-200.0,-5.0]

