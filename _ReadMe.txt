Programmet startas från filen Main.py. Detta är ingången till consolapplikationen.
Sist i Main.py ligger raden som startar programmet, genom att göra ändringar i denna kan man växla från Demo läge till Skarpt Läge.

Variabeln demo_mode anger om applikationen körs i Demoläge eller inte.
Demoläge -    main_menu(Bank(demo_mode=True))
Skarptläge -  main_menu(Bank(demo_mode=True))

Skillnaden mellan demoläge och skarpt läge är hur data läses upp och sparas.

Demoläge
Programmet använder två filer för att spara Customers och Transactions.
En fil för uppläsning av data vid start.
En fil för att skriva data till som tillkommer under tiden applikationen körs.
Vid varje uppstart kommer filen som skrivs till skrivas över med data vilket gör att i Demoläge sparas inte data från tidigare körningar

Skarpt läge
Programmet använder en fil för att spara Customers och Transactions.
Sparat data kommer att sparas från tidigare körningar.
