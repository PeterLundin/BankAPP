import csv
from decimal import Decimal

from Account import Account
from Customer import Customer
from Datasource import Datasource


class Bank:
    
    Customers = []
    
    def __init__(self):
        self._load()
    
    def _load(self):
        #Läser in text filen och befolkar listan som ska innehålla kunderna.
        with open(Datasource().pathToCustomerTxt, 'r',) as file:
            reader = csv.reader(file)
            customers = []
            for row in reader:
                customers.append(self._customer_and_accounts_from_csv(row[0]))
               
            self.Customers = customers
            print(self.Customers[0].Accounts)

    def get_customers(self):
        #Returnerar bankens alla kunder (personnummer och namn) 
        return self.Customers
    def add_customer(name, pnr):
        #Skapar en ny kund med namn och personnummer. Kunden skapas endast om det inte 
        #finns någon kund med personnumret som angetts. Returnerar True om kunden skapades 
        #annars returneras False
        raise Exception("Ej Implementerat")
    def get_customer(self, pnr):
        #Returnerar information om kunden inklusive dennes konton. Första platsen i listan är 
        #förslagsvis reserverad för kundens namn och personnummer sedan följer informationen 
        #om kundens konton.
        for customer in self.Customers:
            if customer.pnr == pnr:
                return customer
            
    def change_customer_name(self, name, pnr):
        #Byter namn på kund, returnerar True om namnet ändrades annars returnerar det False
        #(om kunden inte fanns).
        
        for customer in self.Customers:
            if customer._Pnr == pnr:
                customer.Fullname = name
                customerIndex = self.Customers.index(customer)
                self.Customers[customerIndex] = customer
                return True
            
        return False
    def remove_customer(pnr):
        #Tar bort kund med personnumret som angetts ur banken, alla kundens eventuella konton 
        #tas också bort och resultatet returneras. Listan som returneras ska innehålla information 
        #om alla konton som togs bort, saldot som kunden får tillbaka.
        raise Exception("Ej Implementerat")
    def add_account(pnr):
        #Skapar ett konto till kunden med personnumret som angetts, returnerar kontonumret som 
        #det skapade kontot fick alternativt returneras –1 om inget konto skapades.
        raise Exception("Ej Implementerat")
    def get_account(pnr, account_id):
        #Returnerar Textuell presentation av kontot med kontonummer som tillhör 
        #kunden (kontonummer, saldo, kontotyp).
        raise Exception("Ej Implementerat")
    def deposit(pnr, account_id, amount):
        #Gör en insättning på kontot, returnerar True om det gick bra annars False.
        raise Exception("Ej Implementerat")
    def withdraw(pnr, account_id, amount):
        #Gör ett uttag på kontot, returnerar True om det gick bra annars False.
        raise Exception("Ej Implementerat")
    def close_account(pnr, account_id):
        #Avslutar ett konto. Textuell presentation av kontots saldo ska genereras och 
        #returneras.
        raise Exception("Ej Implementerat")
    
    def get_all_transactions_by_pnr_acc_nr( pnr, acc_nr ):
        #Returnerar alla transaktioner som en kund har gjort med ett specifikt 
        #onto eller -1 om kontot inte existerar.
        raise Exception("Ej Implementerat")

    def _customer_and_accounts_from_csv(self, customerRow):
        customer = self._customer_from_csv(customerRow)
        customer.Accounts = self.accounts_from_csv(customerRow)
        return customer
        
    def _customer_from_csv(self, customerRow):
        customerPart = customerRow.split("#")[0]
        id, fullname, pnr = customerPart.split(":")
        return Customer(fullname, pnr, id)
    
    def accounts_from_csv(self, customerRow):
        accounts = []
        for accaccountPart in customerRow.split("#")[1:]:
            accountNr, accountType, saldo = accaccountPart.split(":")
            account = Account(accountType, Decimal(saldo), int(accountNr))
            accounts.append(account)

        return accounts



bank = Bank()
for c in bank.Customers:
    print(c.toString())
    
success = bank.change_customer_name("Snurre Sprätt", "19721127")
print(success)

for c in bank.Customers:
    print(c.toString())