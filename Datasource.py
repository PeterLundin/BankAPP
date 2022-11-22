from os import path
import csv
from decimal import Decimal

from Account import Account
from Customer import Customer

class Datasource:
    
    pathToCustomerLoadTxt = 'Customer_Load.txt'
    pathToCustomerTxt = 'Customer.txt'
    pathToTransactionsTxt = 'Transactions.txt'

    def datasource_conn(self): 
        # Denna metod implementerar kopplingen till en generisk datasource. Returnerar 
        # en <class ‘tuple’> med en <class ‘bool’> och en <class ‘str’> t.ex., (True, 
        # “Connection successful” [, datasource namn]) 
        if(path.exists(self.pathToCustomerTxt)):
            return (True, "Connection successful",  "txt", self)
        else:
            return (False, "Connection unsuccessful",  "txt", self)
    
    def get_all(self):
        # Returnerar alla kunder i banken.
        with open(Datasource().pathToCustomerLoadTxt, 'r',) as file:
            reader = csv.reader(file)
            customers = []
            for row in reader:
                customers.append(self._customer_and_accounts_from_csv(row[0]))
               
            return customers
    
    def update_by_id(id): 
        # Uppdaterar en kund baserad på id:n som angetts som parameter. Returnerar 
        # info om kunden som uppdaterats, eller -1 om kunden inte finns.
        raise Exception("Ej Implementerat")
    
    def find_by_id(id): 
        # Returnerar en kund baserad på id:n som angetts eller -1 om kunden in finns.
        raise Exception("Ej Implementerat")
    
    def remove_by_id(id):
        # Raderar en kund baserad på id:n som angetts som parameter. Returnerar info 
        # om kunden som tagits bort eller -1 om kunden inte finns.
        raise Exception("Ej Implementerat")
    
    def _customer_and_accounts_from_csv(self, customerRow):
        customer = self._customer_from_csv(customerRow)
        customer.accounts = self.accounts_from_csv(customerRow)
        return customer
        
    def _customer_from_csv(self, customerRow):
        customerPart = customerRow.split("#")[0]
        id, fullname, pnr = customerPart.split(":")
        return Customer(fullname, pnr, id)
    
    def accounts_from_csv(self, customerRow):
        accounts = []
        for accaccountPart in customerRow.split("#")[1:]:
            accountNr, accountType, saldo = accaccountPart.split(":")
            account = Account(accountType, float(saldo), int(accountNr))
            accounts.append(account)

        return accounts
