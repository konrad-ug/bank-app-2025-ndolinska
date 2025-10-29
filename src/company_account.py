from src.account import Account
class Company_Account(Account):
    express_fee = 5.0 
    def __init__(self, company_name, nip):
        self.balance = 0.0
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "INVALID"

    def is_nip_valid(self,nip):
        return isinstance(nip, str) and len(nip) == 10
    
