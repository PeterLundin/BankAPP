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
        customers = []
        with open(Datasource().pathToCustomerLoadTxt, 'r',) as file:
            reader = csv.reader(file)
            
            for row in reader:
                customers.append(self._customer_and_accounts_from_csv(row[0]))
                
            return customers
    
    def write_all(self, customers):
        # skriver alla kunder i banken till fil.
        with open(Datasource().pathToCustomerTxt, 'w', newline='') as file:
            writer = csv.writer(file)
            transactions = []
            for customer in customers:
                writer.writerow([customer.toString()])
                transactions.append(customer.getAllTransactions())

        # skriv alla transactions till fil
        with open(Datasource().pathToTransactionsTxt, 'w', newline='') as file:
            writer = csv.writer(file)
            for transaction in transactions:
                writer.writerow([transaction.toString()])
    
    def update_by_id(self, id, customer): 
        # Uppdaterar en kund baserad på id:n som angetts som parameter. Returnerar 
        # info om kunden som uppdaterats, eller -1 om kunden inte finns.
        customers = self.get_all()
        customer_to_update = None
        for c in customers:
            if c.id == id:
                customer_to_update = c
                
        if customer_to_update is None:
            return -1
        
        customer_to_update = customer
        self.write_all(customers)
        
        return customer
    
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
