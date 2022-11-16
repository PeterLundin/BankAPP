class Customer:

    Fullname = ""
    _Pnr = ""
    Accounts = []
    Transactions = []
  

    def __init__(self, fullname, pnr, id = None, accounts = None, transactions = None):
        self.Fullname = fullname
        self._Pnr = pnr 
        
        if id is None:
            self.Id = self.getId()
        else:
            self.Id = id
            
        if not accounts is None:
            self.Accounts = accounts
        
        if not transactions is None:
            self.Transactions is None
        
    
    def toString(self):
        accounts_toString = ""
        for account in self.Accounts:
            accounts_toString += "#" + account.toString()
            
        return f"{self.Id},{self.Fullname},{self._Pnr}{accounts_toString}"
        