import csv

class IdentityNumbers:
    
    pathToIndentityNumbersTxt = 'IdentityNumbers.txt'
    
    def getCustomerId(self):
        # Läser senaste kund id
        return self.getIdentintityNumber(0)
        
    def getAccountId(self):
        # Läser senaste konto id
        return self.getIdentintityNumber(1)
        
    def getTransactionId(self):
        # Läser senaste transaktions id
        return self.getIdentintityNumber(2)
    
    def getIdentintityNumber(self, index):
        # Returnerar ett uppräknat id baserat på index för det id som efterfrågas
        with open(self.pathToIndentityNumbersTxt, 'r',) as file:
            reader = csv.reader(file)
            identityNumbers = next(reader)[0].split(":")
            identityNumbers[index] = int(identityNumbers[index]) + 1
            self.writeIdentintityNumbers(identityNumbers)
            return int(identityNumbers[index])
        
    def writeIdentintityNumbers(self, identityNumbers):
        # Skriver idn till fil igen
        with open(self.pathToIndentityNumbersTxt, 'w', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow([f"{identityNumbers[0]}:{identityNumbers[1]}:{identityNumbers[2]}"])
    

'''
Tests
id = IdentityNumbers().getCustomerId()
print(id)
id2 = IdentityNumbers().getAccountId()
print(id2)
id3 = IdentityNumbers().getTransactionId()
print(id3)
'''   