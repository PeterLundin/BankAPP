from IdentityNumbers import IdentityNumbers

class Account:
    
    kontotyp = ""
    saldo = 0.0
    kontonummer = None
    
    def __init__(self, kontotyp = "Debit Account", saldo = 0.0, kontonummer = None):
        self.kontotyp = kontotyp
        self.saldo = saldo
        
        if kontonummer is None:
            self.kontonummer = self.getKontonummer()
        else:
            self.kontonummer = kontonummer

    def getKontonummer(self):
        return IdentityNumbers().getAccountId()
    
    def toString(self):
        return f"{self.kontonummer},{self.kontotyp},{self.saldo}"