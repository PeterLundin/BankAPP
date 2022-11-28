from decimal import Decimal

from Account import Account
from Customer import Customer
from Datasource import Datasource
from Transaction import Transaction

class Bank:
    
    customers = []
    transactions = []
    connection = None
    
    def __init__(self):
        self._load()
    
    def _load(self):
        #Läser in text filen och befolkar listan som ska innehålla kunderna.
        connection_info =  Datasource().datasource_conn()
        if connection_info[0]:
            self.connection = connection_info[3]
            db = self.connection.get_all()
            self.customers = db[0]
            self.transactions = db[1]
            
        else:
            raise Exception(connection_info[1])

    def get_customers(self):
        #Returnerar bankens alla kunder (personnummer och namn)
        customers = []
        for customer in self.customers:
            customers.append(f"{customer.getPnr()} - {customer.fullname}")
            
        return customers
    
    def save_customers_and_transactions(self):
        # skriver alla kunder (med konton) samt alla transaktioner till fil
        self.connection.write_all(self.customers, self.transactions)
        
    def save_customers(self):
        # skriver alla kunder (med konton) till fil
        self.connection.write_customers(self.customers)
        
    def save_transactions(self):
        # skriver alla transaktioner till fil
        self.connection.write_transactions(self.transactions)
    
    def add_customer(self, name, pnr):
        #Skapar en ny kund med namn och personnummer. Kunden skapas endast om det inte 
        #finns någon kund med personnumret som angetts. Returnerar True om kunden skapades 
        #annars returneras False
        if self.get_customer_objekt(pnr) is None:
            customer = Customer(name, pnr)
            self.customers.append(customer)
            self.save_customers()
            return True
        else:
            return False

    def get_customer_objekt(self, pnr) -> Customer:
        #Returnerar kunden objektet inklusive dennes konton.
        for customer in self.customers:
            if customer.getPnr() == pnr:
                return customer
            
        return None
    
    def get_customer(self, pnr):
        #Returnerar information om kunden inklusive dennes konton. Första platsen i listan är 
        #förslagsvis reserverad för kundens namn och personnummer sedan följer informationen 
        #om kundens konton.
        customer = self.get_customer_objekt(pnr)
        
        if customer is None:
            return None
        
        customerInformation = []
        customerInformation.append(f"Pnr:{customer.getPnr()} - Name:{customer.fullname} - Total balance:{customer.getBalance()}")
        for account in customer.accounts:
            customerInformation.append(f"Account type:{account.kontotyp} - Account number:{account.kontonummer} - Balance:{account.saldo}")

        return customerInformation
            
    def change_customer_name(self, name, pnr):
        #Byter namn på kund, returnerar True om namnet ändrades annars returnerar det False
        #(om kunden inte fanns).
        customer = self.get_customer_objekt(pnr)
        if customer is not None:
            customer.fullname = name
            self.save_customers()
            return True
        
        return False
    
    def remove_customer(self, pnr):
        #Tar bort kund med personnumret som angetts ur banken, alla kundens eventuella konton 
        #tas också bort och resultatet returneras. Listan som returneras ska innehålla information 
        #om alla konton som togs bort, saldot som kunden får tillbaka.
        customer = self.get_customer_objekt(pnr)
        
        if customer is None:
            return None

        customerIndex = self.customers.index(customer)
        self.customers.pop(customerIndex)
        
        customerInformation = []
        for account in customer.accounts:
            customerInformation.append(f"Account type:{account.kontotyp} - Account number:{account.kontonummer} - Balance:{account.saldo}")
        
        customerInformation.append(f"Closing balance:{customer.getBalance()}")
        
        self.save_customers()
        
        return customerInformation
    
    def add_account(self, pnr):
        #Skapar ett konto till kunden med personnumret som angetts, returnerar kontonumret som 
        #det skapade kontot fick alternativt returneras –1 om inget konto skapades.
        customer = self.get_customer_objekt(pnr)
        account = Account()
        
        if account is not None:
            customer.accounts.append(account)
            self.save_customers()
            return account.kontonummer
        else:
            return -1
    
    def get_account_objekt(self, pnr, account_id):
        #Returnerar account objektet inklusive.
        customer = self.get_customer_objekt(pnr)
        
        for account in customer.accounts:
            if account.kontonummer == account_id:
                return account
            
        return None
    
    def get_account(self, pnr, account_id):
        #Returnerar Textuell presentation av kontot med kontonummer som tillhör 
        #kunden (kontonummer, saldo, kontotyp).
        account = self.get_account_objekt(pnr, account_id)
        if account is not None:
            return f"Account type:{account.kontotyp} - Account number:{account.kontonummer} - Balance:{account.saldo}"
        
        return None
    
    def deposit(self, pnr, account_id, amount):
        #Gör en insättning på kontot, returnerar True om det gick bra annars False.
        account = self.get_account_objekt(pnr, account_id)
        
        if abs(amount) > 0:
            account.saldo += amount
            self.transactions.append(Transaction(pnr, account_id, "deposit", amount))
            self.save_transactions()
            
            return True
        
        return False
    
    def withdraw(self, pnr, account_id, amount):
        #Gör ett uttag på kontot, returnerar True om det gick bra annars False.
        account = self.get_account_objekt(pnr, account_id)
        
        if abs(amount)  <= account.saldo:
            account.saldo -= amount
            self.transactions.append(Transaction(pnr, account_id, "withdraw", amount))
            self.save_transactions()
            
            return True
        
        return False
    
    def close_account(self, pnr, account_id):
        #Avslutar ett konto. Textuell presentation av kontots saldo ska genereras och 
        #returneras.
        customer = self.get_customer_objekt(pnr)
        account = self.get_account_objekt(pnr, account_id)

        accountIndex = customer.accounts.index(account)
        customer.accounts.pop(accountIndex)
        
        self.save_customers()
        
        return f"Closing balance:{account.saldo}"
    
    def get_all_transactions_by_pnr_acc_nr(self, pnr, account_id):
        #Returnerar alla transaktioner som en kund har gjort med ett specifikt 
        #konto eller -1 om kontot inte existerar.
        if self.get_account(pnr, account_id) == None:
            return -1
          
        self.transactions.sort(key=lambda x: (x.pnr, x.account_Id, x.timeStamp))

        customerAccountTransactions = []
        for transaction in self.transactions:
            if transaction.pnr == pnr and transaction.account_Id == account_id:
                customerAccountTransactions.append(f"Time:{transaction.timeStamp} - Account:{transaction.account_Id} - Amount:{transaction.amount} - {transaction.transaction_Type}")
    
        return customerAccountTransactions
        
        

''' Bank tests

bank = Bank()


print("--- Get all customers ---")
cust = bank.get_customers()
for row in cust:
    print(row)

print("--- Add customer that dont exist ---")
success = bank.add_customer("Bruce Lee", "7212121212")
print(success)
print("--- Add customer that exists ---")
success = bank.add_customer("Bruce Peter", "19721127")
print(success)

print("--- Print info about customer---")
gc = bank.get_customer('19721127')
for row in gc:
    print(row)

print("--- Change customer name---")
success = bank.change_customer_name("Snurre Sprätt", "19721127")
print(success)

print("--- Print info about customer ---")
gc = bank.get_customer('19721127')
for row in gc:
    print(row)

print("--- Get all customers---")
cust = bank.get_customers()
for row in cust:
    print(row)
    
print("--- Remove customer---")
rc = bank.remove_customer('7212121212')
for row in rc:
    print(row)

print("--- Get all customers---")    
cust = bank.get_customers()
for row in cust:
    print(row)

print("--- Add account---")       
account_id = bank.add_account('19721127')
print(account_id)

print("--- Print info about customer ---")
gc = bank.get_customer('19721127')
for row in gc:
    print(row)

print("--- Get account ---")
ga = bank.get_account('19721127', 1001)
print(ga)

print("--- Deposit positiv value ---")
success = bank.deposit('19721127', 1001, 50000.0)
print(success)

print("--- Deposit negativ value ---")
success = bank.deposit('19721127', 1001, -750000.0)
print(success)

print("--- Get account ---")
ga = bank.get_account('19721127', 1001)
print(ga)

print("--- Withdraw positiv value ---")
success = bank.withdraw('19721127', 1001, 50000.0)
print(success)

print("--- Withdraw negativ value ---")
success = bank.withdraw('19721127', 1001, -750000.0)
print(success)

print("--- Get account ---")
ga = bank.get_account('19721127', 1001)
print(ga)

print("--- Close account ---")
message = bank.close_account('19721127', 1003)
print(message)

print("--- Print info about customer ---")
gc = bank.get_customer('19721127')
for row in gc:
    print(row)
    

print("--- Withdraw and Deposit some values---")
success = bank.withdraw('19721127', 1001, 10000.0)
success = bank.withdraw('19721127', 1001, 15000.0)
success = bank.deposit('19721127', 1001, 15000.0)
success = bank.deposit('19721127', 1001, 10000.0)

success = bank.withdraw('19740709', 1004, 10000.0)
success = bank.withdraw('19740709', 1004, 15000.0)
success = bank.deposit('19740709', 1005, 15000.0)
success = bank.deposit('19740709', 1004, 10000.0)

print("--- pnr 19721127 and account_id 1001 ---")
transisar = bank.get_all_transactions_by_pnr_acc_nr('19721127', 1001)
for trans in transisar:
    print(trans)
    
print("--- pnr 19740709 and account_id 1004 ---")
transisar = bank.get_all_transactions_by_pnr_acc_nr('19740709', 1004)
for trans in transisar:
    print(trans)
    
    
'''