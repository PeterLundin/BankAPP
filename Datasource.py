import datetime
from os import path
import csv
from decimal import Decimal

from Account import Account
from Customer import Customer
from Transaction import Transaction

class Datasource:
    
    pathToCustomerLoadDemoTxt = 'Customer_Load_Demo.txt'
    pathToCustomerSaveDemoTxt = 'Customer_Save_Demo.txt'
    pathToTransactionsLoadDemoTxt = 'Transactions_Load_Demo.txt'
    pathToTransactionsSaveDemoTxt = 'Transactions_Save_Demo.txt'
    pathToCustomerTxt = 'Customer.txt'
    pathToTransactionsTxt = 'Transactions.txt'
    demoMode = False

    def datasource_conn(self, demoMode = False): 
        # Denna metod implementerar kopplingen till en generisk datasource. Returnerar 
        # en <class ‘tuple’> med en <class ‘bool’> och en <class ‘str’> t.ex., (True, 
        # “Connection successful” [, datasource namn]) 
        
        self.demoMode = demoMode
        
        if(path.exists(self.datasource_customers_load_txt_path())):
            return (True, "Connection successful",  "txt", self)
        else:
            return (False, "Connection unsuccessful",  "txt", self)
    
    def datasource_customers_load_txt_path(self):
        # Returnerar rätt sökväg till textfilen om det är Demoläge eller inte
        if self.demoMode:
            return self.pathToCustomerLoadDemoTxt
        else:
            return self.pathToCustomerTxt
        
    def datasource_customers_save_txt_path(self):
        # Returnerar rätt sökväg till textfilen om det är Demoläge eller inte
        if self.demoMode:
            return self.pathToCustomerSaveDemoTxt
        else:
            return self.pathToCustomerTxt
        
    def datasource_transactions_load_txt_path(self):
        # Returnerar rätt sökväg till textfilen om det är Demoläge eller inte
        if self.demoMode:
            return self.pathToTransactionsLoadDemoTxt
        else:
            return self.pathToTransactionsTxt
        
    def datasource_transactions_save_txt_path(self):
        # Returnerar rätt sökväg till textfilen om det är Demoläge eller inte
        if self.demoMode:
            return self.pathToTransactionsLoadDemoTxt
        else:
            return self.pathToTransactionsTxt
    
    def get_all(self):
        # Returnerar alla kunder och transaktioner i banken.
        customers = self.get_all_customers()
        transactions = self.get_all_transactions()
                
        return (customers, transactions)

    def get_all_customers(self):        
        # Returnerar alla kunder i banken.
        customers = []
        with open(self.datasource_customers_load_txt_path(), 'r',) as file:
            reader = csv.reader(file)
            
            for row in reader:
                customers.append(self._customer_and_accounts_from_csv(row[0]))
                
            return customers
        
    def get_all_transactions(self):
        # Returnerar alla transaktioner i banken.
        transactions = []
        with open(self.datasource_transactions_load_txt_path(), 'r',) as file:
            reader = csv.reader(file)
            for row in reader:
                transactions.append(self._transactions_from_csv(row[0]))
                
            return transactions
    
    def write_all(self, customers, transactions):
        # skriver alla kunder och transaktioner i banken till fil.
        self.write_customers(customers)
        self.write_transactions(transactions)

    def write_transactions(self, transactions):
        # skriv alla transactions till fil
        with open(self.datasource_transactions_save_txt_path(), 'w', newline='') as file:
            writer = csv.writer(file)
            for transaction in transactions:
                writer.writerow([transaction.toString()])
              
    def write_customers(self, customers):
        # skriver alla kunder i banken till fil.
        with open(self.datasource_customers_save_txt_path(), 'w', newline='') as file:
            writer = csv.writer(file)
            for customer in customers:
                writer.writerow([customer.toString()])
    
    def update_by_id(self, id, customer): 
        # Uppdaterar en kund baserad på id:n som angetts som parameter. Returnerar 
        # info om kunden som uppdaterats, eller -1 om kunden inte finns.
        customers = self.get_all()
        customer_to_update = None
        for customer in customers:
            if customer.id == id:
                customer_to_update = customer
                
        if customer_to_update is None:
            return -1
        
        customer_to_update = customer
        self.write_all(customers)
        
        return customer
    
    def find_by_id(self, id): 
        # Returnerar en kund baserad på id:n som angetts eller -1 om kunden in finns.
        customers = self.get_all()
        for customer in customers:
            if customer.id == id:
                return customer

        return -1
    
    def remove_by_id(self, id):
        # Raderar en kund baserad på id:n som angetts som parameter. Returnerar info 
        # om kunden som tagits bort eller -1 om kunden inte finns.
        customers = self.get_all()
        customer_to_delete = None
        for customer in customers:
            if customer.id == id:
                customer_to_delete = customer
                
        if customer_to_delete is None:
            return -1
        
        customers.pop(customer_to_delete)
        self.write_all(customers)
        
        return customer
    
    def _customer_and_accounts_from_csv(self, customerRow):
        customer = self._customer_from_csv(customerRow)
        customer.accounts = self._accounts_from_csv(customerRow)
        return customer
        
    def _customer_from_csv(self, customerRow):
        customerPart = customerRow.split("#")[0]
        id, fullname, pnr = customerPart.split(":")
        return Customer(fullname, pnr, id)
    
    def _accounts_from_csv(self, customerRow):
        accounts = []
        for accaccountPart in customerRow.split("#")[1:]:
            accountNr, accountType, saldo = accaccountPart.split(":")
            account = Account(accountType, float(saldo), int(accountNr))
            accounts.append(account)

        return accounts
    
    def _transactions_from_csv(self, transactionRow):
        transaction = None
        pnr, account_Id, transaction_Type, amount, str_timeStamp = transactionRow.split(";")
        timeStamp = datetime.datetime.strptime(str_timeStamp, '%Y-%m-%d %H:%M:%S.%f')
        transaction = Transaction(pnr, int(account_Id), transaction_Type, float(amount), timeStamp)

        return transaction
