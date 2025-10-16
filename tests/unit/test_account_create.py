from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "5443222277")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0

    def test_pesel_too_long(self):
        account = Account("John", "Doe", "5443222271232327")
        assert account.pesel == "INVALID"
    
    def test_pesel_too_short(self):
        account = Account("John", "Doe", "5442717")
        assert account.pesel == "INVALID"
    
    def test_pesel_none(self):
        account= Account("John", "Doe", None)
        assert account.pesel == "INVALID"
    
    def test_promo_code_age_viable(self):
        account= Account("John", "Doe", "6734567891", "PROM_XYZ")
        assert account.balance == 50.0

    def test_promo_code_age_viable_21stcen(self):
        account= Account("John", "Doe", "0934567891", "PROM_XYZ")
        assert account.balance == 50.0

    def test_promo_code_age_not_viable(self):
        account= Account("John", "Doe", "581567891", "PROM_XYZ")
        assert account.balance == 0.0

    def test_promo_code_none(self):
        account= Account("John", "Doe", "1234567891", None)
        assert account.balance == 0.0

    def test_promo_code_suffix_too_long(self):
        account= Account("John", "Doe", "1234567891", "PROM_XYZYA")
        assert account.balance == 0.0

    def test_promo_code_suffix_too_short(self):
        account= Account("John", "Doe", "1234567891", "PROM_XA")
        assert account.balance == 0.0

    def test_promo_code_prefix_wrong(self):
        account= Account("John", "Doe", "1234567891", "PRM_XYZ")
        assert account.balance == 0.0
  