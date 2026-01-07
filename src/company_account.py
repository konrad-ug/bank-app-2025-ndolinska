import os
import datetime
import requests
from src.account import Account
class Company_Account(Account): # pragma: no cover
    express_fee = 5.0 
    def __init__(self, company_name, nip):
        self.balance = 0.0
        self.company_name = company_name
        if not self.is_nip_valid(nip):
            self.nip = "INVALID"
        elif self.verify_nip(nip):
            self.nip=nip
        else:
            raise ValueError("Company not registered!!")
        self.history=[]

    def is_nip_valid(self,nip):
        return isinstance(nip, str) and len(nip) == 10
    
    def take_loan(self,amount):
        if self.balance>=amount*2 and -1775 in self.history:
            self.balance += amount
            return True
        return False
    
    def verify_nip(self, nip):
        today = datetime.date.today().strftime("%Y-%m-%d")
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
        if not base_url[-1]=="/":
            base_url += "/"
        endpoint = f"{base_url}api/search/nip/{nip}?date={today}"
        try:
            response = requests.get(endpoint)
            data = response.json()
            print(f"API Response for NIP {nip}: {data}")
            result = data.get("result", {})
            subject = result.get("subject")
            if subject and subject.get("statusVat") == "Czynny":
                return True
            return False
        except requests.RequestException as e:
            print(f"API Connection Error: {e}")
            return False

    
