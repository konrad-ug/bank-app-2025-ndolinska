from src.personal_account import Personal_Account
from typing import List

class AccountRegistry:
    def __init__(self):
        self.accounts: List[Personal_Account] = []

    def add_account(self, account: Personal_Account):
        self.accounts.append(account)

    def search_account(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None
    
    def get_all(self):
        return self.accounts
    
    def return_length(self):
        return len(self.accounts)