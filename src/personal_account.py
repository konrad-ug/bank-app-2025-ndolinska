from src.account import Account
class Personal_Account(Account):
    express_fee = 1.0 
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "INVALID"
        self.balance = 50.0 if self.check_promo_code(promo_code) and self.check_age_viable(pesel) else 0.0
    
    def is_pesel_valid(self,pesel):
        return isinstance(pesel, str) and len(pesel) == 11
    
    def check_promo_code(self,promo_code):
        return isinstance(promo_code, str) and promo_code[:5]  == "PROM_" and len(promo_code) == 8
    
    def check_age_viable(self,pesel):
        return int(pesel[:2]) > 60 or int(pesel[2]) > 2
