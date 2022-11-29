from os import system
from Bank import Bank

def clear_screen():
    system('cls')
    
def is_float(element: any):
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

    
    
def main_menu(bank):
    clear_screen()
    while True:
        print('------------------------------------------------------')
        print('------------- Bank - Huvudmeny -----------------------')
        print('------------------------------------------------------')
        print('  1 - Lista alla kunder')
        print('  2 - Ny kund')
        print('  3 - Ta bort kund')
        print('  4 - Kundmeny -> Hantera kund uppgifter')
        print('  0 - Avsluta')
        print('------------------------------------------------------')
        print('')
        
        menyval = input('Menyval: ')
        
        # Printa en lista med bankens kunder (personnummer, för och efternamn)
        if menyval.strip() == '1':
            clear_screen()
            customers = bank.get_customers()
            print('1 - Lista alla kunder')
            for customer in customers:
                print(customer)
        
        # Lägga till en ny kund med ett unikt personnummer.
        elif menyval.strip() == '2':
            clear_screen()
            validated = False
            pnr = 0
            name = None
            
            print('2 - Ny kund')
            while validated == False:
                pnr = input("Ange kundens födelsenummer (YYYYMMDDXXXX): ")
                
                if len(pnr) == 12 and pnr.isnumeric() and (pnr[:2] == '19' or pnr[:2] == '20'):
                    validated = True
                else:
                    print('Felaktigt Födelsenummer!')
            
            validated = False
            while validated == False:    
                name = input("Ange kundens namn: ")
                
                if len(name) >= 2 and not name.isnumeric():
                    validated = True
                else:
                    print('Felaktigt Namn!')
                    
            success = bank.add_customer(name, pnr)
            if not success: 
                print("Kunden kunde inte läggas till!")

        # Ta bort en befintlig kund, befintliga konton måste också avslutas.
        elif menyval.strip() == '3':
            print('3 - Ta bort kund')
            pnr = input("Ange födelsenummer för kunden som ska tas bort (YYYYMMDDXXXX): ")
            
            result = bank.remove_customer(pnr)
            
            if result is None:
                print("Ingen kund med det födelsenumret hittades")
                
            else:
                print("Information om kunden som togs bort:")
                for row in result:
                    print(row)
        
        # print('  4 - Hantera kund uppgifter')
        elif menyval.strip() == '4':
            print('4 - Kundmeny -> Hantera kund uppgifter')
            pnr = input("Ange födelsenummer för kunden som ska hanteras (YYYYMMDDXXXX): ")
            
            customer = bank.get_customer_objekt(pnr)
            
            if customer is None:
                print("Ingen kund med det födelsenumret hittades")
                
            else:
                customer_menu(bank, pnr)
            
        elif menyval.strip() == '0':
            clear_screen()
            break
        
def customer_menu(bank, pnr):
    clear_screen()
    while True:
        print('------------------------------------------------------')
        print(f'------------- Kundmeny - {pnr} --------------')
        print('------------------------------------------------------')
        print('  1 - Se kund information')
        print('  2 - Ändra kundnamn')
        print('  3 - Skapa konto')
        print('  4 - Avsluta konto')
        print('  5 - Kontomeny -> insättning/uttag/transaktions historik')
        print('  0 - Tillbaks till huvudmeny')
        print('  00 - Avsluta')
        print('------------------------------------------------------')
        print('')
        
        menyval = input('Menyval: ')
        
        # Se information om vald kund inklusive alla konton (kontonummer, saldo, kontotyp).
        if menyval.strip() == '1':
            print('1 - Se kund information')
            customerInformation = bank.get_customer(pnr)
            for row in customerInformation:
                print(row)
                
        # Ändra en kunds namn (personnummer ska inte kunna ändras).
        elif menyval.strip() == '2':
            print('2 - Ändra kundnamn')

            validated = False
            while validated == False:    
                name = input("Ange kundens namn: ")
                
                if len(name) >= 2 and not name.isnumeric():
                    validated = True
                else:
                    print('Felaktigt Namn!')
                    
            bank.change_customer_name(name, pnr)
            
            
        # ● Skapa konto (Account) till en befintlig kund, ett unikt kontonummer genereras (VG)(första kontot får nummer 1001, nästa 1002 osv.).
        elif menyval.strip() == '3':
            print('3 - Skapa konto')
            kontonummer = bank.add_account(pnr)
             
            if kontonummer == -1:
                print("Konto kunde inte skapas.")
            else:
                print(f"Konto med kontonummer: {kontonummer} skapades")
            
        # Avsluta Konto via kontonummer attributet, saldo skrivs ut och kontot tas bort.
        elif menyval.strip() == '4':
            print('4 - Avsluta konto')
            kontonummer = input("Ange kontonummer på kontot som ska avslutas:")
            
            if bank.get_account_objekt(pnr, int(kontonummer)) is None:
                print(f"Kunde inte hitta kontot med nummer {kontonummer}")                
            else:
                saldo = bank.close_account(pnr, int(kontonummer))
                print(f"Konto {kontonummer} avslutades")
                print(saldo)
            
        # Hantera specifikt konto
        elif menyval.strip() == '5':
            print('5 - Kontomeny -> insättning/uttag/transaktions historik')
            kontonummer = input("Ange kontonummer som ska hanteras:")
            
            if bank.get_account_objekt(pnr, int(kontonummer)) is None:
                print(f"Kunde inte hitta kontot med nummer {kontonummer}")                
            else:
                customer_account_menu(bank, pnr, int(kontonummer))
                
        elif menyval.strip() == '0':
            clear_screen()
            break
        
        elif menyval.strip() == '00':
            clear_screen()
            quit()
            
def customer_account_menu(bank, pnr, kontonummer):
    clear_screen()
    account = bank.get_account_objekt(pnr, kontonummer)
    while True:
        print('------------------------------------------------------')
        print(f'------ Kontomeny - {pnr} -------------------')
        print(f'------ Kontonummer: {kontonummer}: Saldo: {account.saldo} ------')
        print('------------------------------------------------------')
        print('  1 - Sätt in pengar')
        print('  2 - Ta ut pengar')
        print('  3 - Visa transationer')
        print('  0 - Tillbaks till kundmenyn')
        print('  00 - Avsluta')
        print('------------------------------------------------------')
        print('')
        
        menyval = input('Menyval: ')
        
        # Sätta in pengar på ett konto.
        if menyval.strip() == '1':
            print('1 - Sätt in pengar')
            belopp = input("Ange beloppet du vill sätta in: ")
            
            if(is_float(belopp)):
                success = bank.deposit(pnr, kontonummer, float(belopp))
            
                if success:
                    print(f"{belopp} insatt på kontot {kontonummer}.")
                else:
                    print(f"Kunde inte sätta in {belopp} på kontot {kontonummer}.")
            else:
                print(f"Beloppet {belopp} är inte korrekt angiven!")

   
        # Ta ut pengar från kontot (men bara om saldot täcker uttagsbeloppet).
        elif menyval.strip() == '2':
            print('2 - Ta ut pengar')
            belopp = input("Ange beloppet du vill ta ut: ")
            
            if(is_float(belopp)):
                success = bank.withdraw(pnr, kontonummer, float(belopp))
            
                if success:
                    print(f"{belopp} uttaget från kontot {kontonummer}.")
                else:
                    print(f"Kunde inte ta ut {belopp} från kontot {kontonummer}.")
            else:
                print(f"Beloppet {belopp} är inte korrekt angiven!")
            
            
        # Se alla transaktioner en kund har gjort med ett specifikt konto
        elif menyval.strip() == '3':
            transactions = bank.get_all_transactions_by_pnr_acc_nr(pnr, kontonummer)
            print(f"Alla transationer gjorda med konto {kontonummer}")
            for transaction in transactions:
                print(transaction)

        elif menyval.strip() == '0':
            clear_screen()
            break
        
        elif menyval.strip() == '00':
            clear_screen()
            quit()
        
    
# Startar och kör programmet   
    

main_menu(Bank(demo_mode=True))