class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def transfer_incoming(self,amount):
        if isinstance(amount,(float,int)) and amount > 0.0:
            self.balance += amount
            self.history.append(amount)
            return True
        return False
    
    def transfer_outgoing(self,amount): 
        if isinstance(amount,(float,int)) and (amount > 0.0 and amount <= self.balance):
            self.balance -= amount
            self.history.append(-amount)
            return True
        return False

    def transfer_express_outgoing(self, amount):
        fee = getattr(self, "express_fee", 0.0)
        if isinstance(amount, (float, int)) and amount > 0.0:
            if self.balance + fee >= amount:
                self.balance -= (amount + fee)
                self.history.append(-amount)
                self.history.append(-fee)
                return True
        return False
    