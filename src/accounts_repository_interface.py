from abc import ABC, abstractmethod
from typing import List, Any
from dataclasses import dataclass

@dataclass
class Account:
    id: int
    owner: str
    balance: float

class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self, accounts: List[Account]) -> None:
        pass

    @abstractmethod
    def load_all(self) -> List[Account]:
        pass