from src.accounts_repository_interface import Account, AccountsRepository
import pytest

def test_account_dataclass_structure():
    acc = Account(id=1, owner="Test Owner", balance=100.0)
    assert acc.id == 1
    assert acc.owner == "Test Owner"
    assert acc.balance == 100.0

def test_cannot_instantiate_abstract_repository():
    with pytest.raises(TypeError):
        # Nie można stworzyć instancji klasy z metodami abstrakcyjnymi
        AccountsRepository()
        
def test_abstract_methods_body_execution():
    class TestRepo(AccountsRepository):
        def save_all(self, accounts):
            super().save_all(accounts)

        def load_all(self):
            return super().load_all()

    repo = TestRepo()

    repo.save_all([])
    result = repo.load_all()
    assert result is None