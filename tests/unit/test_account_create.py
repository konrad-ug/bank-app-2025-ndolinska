from src.personal_account import Personal_Account
from src.company_account import Company_Account
from pytest_mock import MockFixture

#====================TESTY TWORZENIA PERSONAL ACCOUNT ===============================
class TestPersonalAccount:
    def test_account_creation(self):
        account = Personal_Account("John", "Doe", "5443222277")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0

    def test_pesel_too_long(self):
        account = Personal_Account("John", "Doe", "5443222271232327")
        assert account.pesel == "INVALID"
    
    def test_pesel_too_short(self):
        account = Personal_Account("John", "Doe", "5442717")
        assert account.pesel == "INVALID"
    
    def test_pesel_none(self):
        account= Personal_Account("John", "Doe", None)
        assert account.pesel == "INVALID"
    
    def test_promo_code_age_viable(self):
        account= Personal_Account("John", "Doe", "6734567891", "PROM_XYZ")
        assert account.balance == 50.0

    def test_promo_code_age_viable_21stcen(self):
        account= Personal_Account("John", "Doe", "0934567891", "PROM_XYZ")
        assert account.balance == 50.0

    def test_promo_code_age_not_viable(self):
        account= Personal_Account("John", "Doe", "581567891", "PROM_XYZ")
        assert account.balance == 0.0

    def test_promo_code_none(self):
        account= Personal_Account("John", "Doe", "1234567891", None)
        assert account.balance == 0.0

    def test_promo_code_suffix_too_long(self):
        account= Personal_Account("John", "Doe", "1234567891", "PROM_XYZYA")
        assert account.balance == 0.0

    def test_promo_code_suffix_too_short(self):
        account= Personal_Account("John", "Doe", "1234567891", "PROM_XA")
        assert account.balance == 0.0

    def test_promo_code_prefix_wrong(self):
        account= Personal_Account("John", "Doe", "1234567891", "PRM_XYZ")
        assert account.balance == 0.0

#====================TESTY TWORZENIA COMPANY ACCOUNT ===============================
class TestCompanyAccount:
    def test_company_account_creation(self, mocker:MockFixture ):
        mocker.patch.object(Company_Account, 'verify_nip', return_value=True)
        company_account = Company_Account("JANUSZEX", "1234567890")
        assert company_account.company_name == "JANUSZEX"
        assert company_account.balance == 0.0
        assert company_account.nip == "1234567890"
        
    def test_nip_too_long(self):
        account = Company_Account("ABC","5443222271232327")
        assert account.nip == "INVALID"
    
    def test_nip_too_short(self):
        account = Company_Account("ABC", "5442717")
        assert account.nip == "INVALID"
    
    def test_nip_none(self):
        account= Company_Account("ABC", None)
        assert account.nip == "INVALID"
    def test_nip_not_str(self):
        account= Company_Account("ABC", "lalalala")
        assert account.nip == "INVALID"
        
