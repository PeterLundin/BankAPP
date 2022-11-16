
class Account:
    
    def __init__(self, kontotyp = "Debit Account", saldo = 0.0, kontonummer = None):
        self.Kontotyp = kontotyp
        self.Saldo = saldo
        
        if kontonummer is None:
            self.Kontonummer = self.getKontonummer()
        else:
            self.Kontonummer = kontonummer
            
    
    def getKontonummer(self):
        return 123456
    
    def toString(self):
        return f"{self.Kontonummer},{self.Kontotyp},{self.Saldo}"