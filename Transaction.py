from datetime import datetime

class Transaction:
    
    def __init__(self, pnr, account_Id, transaction_Type, amount, timeStamp = None):
        self.pnr = pnr
        self.account_Id = account_Id
        self.transaction_Type = transaction_Type
        self.amount = amount
        if timeStamp is None:
            self.timeStamp = datetime.now()
        else:
            self.timeStamp = timeStamp
        
    def toString(self):
        return f"{self.pnr};{self.account_Id};{self.transaction_Type};{self.amount};{self.timeStamp}"