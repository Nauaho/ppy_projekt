from baza_danych.BazaDanych import BazaDanych, Zadanie, ZadanieKratka
import datetime

path = "baza_danych\\dane\\dane.db"

db = BazaDanych(path)

dziala = True
while dziala:
    login = None
    admin = False

    while login is None and dziala:
        odp = input("Jeżeli chciał byś się:\n"
                    "zarejestrowć wpisz Rejestruj\n"
                    "zalogować wpisz Zaloguj\n"
                    "opóścić program wpisz Wyjdź\n")
        if odp == 'Rejestruj' or odp == 'Zaloguj':
            podanyLogin = input("Podaj login:\n")
            haslo = input("Podaj hasło:\n")
            if odp == 'Rejestruj':
                login = db.zarejestruj_sie(podanyLogin, haslo)
            else:
                login = db.zaloguj_sie(podanyLogin, haslo)
            if login is None:
                print("Podano złe informacje proszę spróbować ponownie.")
            else:
                if db.admin_o_takim_loginie(login) is not None:
                    admin = True
        elif odp == 'Wyjdź':
            dziala = False
            print("Program zotanie zamknięty.")
        else:
            print("Proszę wybrać jedną z podanych opcji.")

    while login is not None and dziala:
        print("Możliwe czynności do wykonania to, wpisz:\n"
              "Usuń - jeżeli chciał byś usunąć zadanie\n"
              "Dodaj - jeżeli chciał byś dodać zadanie\n"
              "Zobacz - jeżeli chciał byś zobaczyć zadanie\n"
              "Edytuj - jeżeli chciał byś edytować zadanie\n"
              "Wyjdź - jeżeli chciał byś wyjść z programu\n"
              "Wyloguj - jeżeli chciał byś się wylogować")
        if admin:
            print("Dodaj admina - jeżeli chciał byś dodać nowego administratora")
        odp = input("Proszę wpisać wybraną odpowiedź poniżej:\n")

        if odp == "Usuń":
            id = input("Proszę podać id zadania do usunięcia:\n")
            doWyswietlenia = db.usun_zadanie(id)
            print(doWyswietlenia)
        elif odp == "Dodaj":
            tytul = input("Proszę wpisać tytuł zadania:\n")
            opis = input("Poreszę wpisac opis zadania:\n")
            adminP = input("Podaj nazwę administrator (jeżeli nie chcesz wprowadzać naciśnij Enater):\n") or None
            status = input("Podaj status (w trakcie/zakończone)(jeżeli chcesz zostawić status do zrobienia naciśnij Enter):\n") or "do zrobienia"
            priorytet = input("Podaj priorytet (nizki/wysoki)(jeżeli chcesz zostawić priorytet średni naciśnij Enter):\n") or "średni"
            deadline = datetime.datetime.now() + datetime.timedelta(days=1)
            wybor = input("Jeżeli chciał byś przpisać inną datę zakończenia niż jutro, napisz tak:\n")
            if wybor == "tak":
                deadline = None
                while deadline is None:
                    try:
                        dni = int(input("Wpisz liczbę dni:\n"))
                        deadline = datetime.datetime.now() + datetime.timedelta(days=dni)
                    except ValueError:
                        print("Nie została wprowadzona liczba całkowita.")
            doWyswietlenia = db.dodaj_zadanie(login, tytul, opis, adminP, status, priorytet, deadline=deadline)
            print(doWyswietlenia)
        elif odp == "Zobacz":
            doWyswietlenia = ""
            wybor = input("Jeżeli chcesz filtrować zadania przez status napisz tak:\n")
            if wybor == "tak":
                status = input("Wpisz jeden z poniszych:\n"
                               "->do zrobienia\n"
                               "->w trakcie\n"
                               "->zakończone\n")
                doWyswietlenia = db.daj_zadania(login, predykat=(lambda zadania : zadania.status == status))
            else:
                doWyswietlenia = db.daj_zadania(login)
            for pozycja in doWyswietlenia:
                print("Id: " + str(pozycja.id) +
                      "\nAdministrator: " + str(pozycja.admin) +
                      "\nTytuł: " + pozycja.tytul +
                      "\nOpis: " + pozycja.opis +
                      "\nData powstania: " + str(pozycja.data_utworzenia) +
                      "\nData zakończenia: " + str(pozycja.deadline) +
                      "\nPriorytet: " + pozycja.priorytet +
                      "\nStatus: " + pozycja.status + "\n")
        elif odp == "Edytuj":
            id = None
            while id is None:
                try:
                    id = int(input("Podaj id zadania do zmiany:\n"))
                except ValueError:
                    print("Podana wartość nie jest liczbą całkowitą.")
            print("Wpisz informacjie które chcesz żeby były zpisane w tym zadaniu.")
            tytul = input("Podaj tytuł zadania:\n")
            opis = input("Podaj opis adania:\n")
            adminP = input("Podaj wybranego administratora(jeżli chcesz pominąć kliknij Enter):\n") or None
            status = input("Napisz jeden z podanych statusów:\n"
                           "->do zrobienia\n"
                           "->w trakcie\n"
                           "->zakończone\n")
            priorytet = input("Napisz jeden z podanych priorytetów:\n"
                              "->nizki\n"
                              "->średni\n"
                              "->wysoki\n")
            dataUtworzenia = None
            while dataUtworzenia is None:
                try:
                    data = int(input("Podaj ile dni temu zadanie zostało przypisane:\n"))
                    dataUtworzenia = str(datetime.datetime.now() - datetime.timedelta(days=data))
                except ValueError:
                    print("Podana wartość nie jest liczbą całkowitą.")
            deadline = None
            while deadline is None:
                try:
                    data = int(input("Podaj za ile dni zadanie się zakończy:\n"))
                    deadline = str(datetime.datetime.now() + datetime.timedelta(days=data))
                except ValueError:
                    print("Podana wartość nie jest liczbą całkowitą.")
            zadanie = Zadanie(ZadanieKratka(id, status, priorytet, adminP, tytul, opis, dataUtworzenia, deadline))
            doWyswietlenia = db.edytuj_zadanie(zadanie)
            print(doWyswietlenia)
        elif odp == "Wyjdź":
            dziala = False
            print("Program zotanie zamknięty.")
        elif odp == "Wyloguj":
            login = None
            print("Zostałeś wylogowany.")
        elif odp == "Dodaj admina":
            nowyAdmin = input("Podaj login nowego administratora:\n")
            doWyswietlenia = db.dodaj_admina(login, nowyAdmin)
            print(doWyswietlenia)
        else:
            print("Podano nie właściwą komendę proszę spróbować ponownie.")

