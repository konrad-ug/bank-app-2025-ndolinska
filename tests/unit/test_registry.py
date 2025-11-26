from src.account_registry import AccountRegistry
from src.personal_account import Personal_Account
import pytest # pyright: ignore[reportMissingImports]

class TestAccountRegistry:
    @pytest.fixture
    def registry(self):
        return AccountRegistry()

    def test_add_and_search_account(self,registry:AccountRegistry):
        acc= Personal_Account("John","Doe","12345678901")
        registry.add_account(acc)
        retrieved=registry.search_account("12345678901")
        assert retrieved == acc

    def test_acc_not_found(self,registry:AccountRegistry):
        retrieved=registry.search_account("00000000000")
        assert retrieved is None

    def test_get_all_accounts(self,registry:AccountRegistry):
        acc1= Personal_Account("John","Doe","12345678901")
        acc2= Personal_Account("Jane","Doe","12345678910")
        registry.add_account(acc1)
        registry.add_account(acc2)
        all_accounts = registry.get_all()
        assert all_accounts == [acc1, acc2]

    def test_get_account_count(self,registry:AccountRegistry):
        acc1= Personal_Account("John","Doe","12345678901")
        acc2= Personal_Account("Jane","Doe","12345678910")
        registry.add_account(acc1)
        registry.add_account(acc2)
        count = registry.return_length()
        assert count == 2
