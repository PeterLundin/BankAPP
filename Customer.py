from IdentityNumbers import IdentityNumbers

class Customer:

    fullname = None
    _pnr = None
    id = None
    accounts = []

    def __init__(self, fullname, pnr, id = None):
        self.fullname = fullname
        self._pnr = pnr 
        
        if id is None:
            self.id = self.getCustomerId()
        else:
            self.id = id

    def getPnr(self):
        return self._pnr
    
    def getBalance(self):
        balance = 0.0
        for account in self.accounts:
            balance += account.saldo
            
        return balance
    
    def getAllTransactions(self):
        transactions = []
        for account in self.accounts:
            transactions.append(account.transactions)
            
        transactions.sort(key=lambda x: (x.pnr, x.account_Id, x.timeStamp))
        
        return transactions
    
    def getCustomerId(self):
        return IdentityNumbers().getCustomerId()
    
    def toString(self):
        accounts_toString = ""
        for account in self.accounts:
            accounts_toString += "#" + account.toString()
            
        return f"{self.id},{self.fullname},{self._pnr}{accounts_toString}"
        