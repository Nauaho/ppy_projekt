from baza_danych import hasher, tworzenie
import sqlite3
import datetime

class BazaDanych:

    def __init__(self, path):
        self.bd = tworzenie.init(path)
    
    def zarejestruj_sie(self, login, haslo):
        uzytkownik = self.__uzytkownik_o_takim_loginie(login)
        if(uzytkownik != None):
            return None
        sql = "INSERT INTO Uzytkownicy VALUES(?,?,?);"
        self.bd.execute(sql, hasher.uzytkownik_sol_i_haslo(login, haslo))
        return login

    def zaloguj_sie(self, login, haslo):
        uzytkownik = self.__uzytkownik_o_takim_loginie(login)
        if(uzytkownik == None):
            return None
        login = uzytkownik[0]
        sol = uzytkownik[1]
        haslo_haszowane = uzytkownik[2]
        if(hasher.weryfikuj_haslo(sol, haslo, haslo_haszowane)):
            return login
        else:
            return None

    def __uzytkownik_o_takim_loginie(self, login):
        sql = "SELECT * FROM Uzytkownicy WHERE login = ?;" 
        login = (login,)
        cursor = self.bd.cursor()
        cursor.execute(sql, login)
        user = cursor.fetchall()
        if(len(user) == 0):
            return None
        else:
            return user[0]
        
    def admin_o_takim_loginie(self, login):
        sql = "SELECT * FROM Adminy WHERE login = ?;"
        login = (login,)
        cursor = self.bd.cursor()
        cursor.execute(sql, login)
        admin = cursor.fetchall()
        if(len(admin) == 0):
            return None
        else:
            return admin[0][0]
        
    def usun_zadanie(self,id):
        sql = "DELETE FROM Zadania WHERE id = ?;"
        id = (id,)
        c = self.bd.execute(sql, id)
        self.bd.commit()
        if(c.rowcount == 0):
            return "Zadania o takim identyfikatorze nie istnieje"
        else:
            return "Zadanie zostało usunięte"
        
    def dodaj_zadanie(self, login, tytul, opis,
                    admin = None,
                    status = 'do zrobienia',
                    priorytet = 'średni',
                    data_utworzenia = datetime.datetime.now(),
                    deadline = datetime.datetime.now() + datetime.timedelta(days = 1)):
        try:
            zadanie = (None, 
                    status, priorytet,
                    login, admin,
                    tytul, opis,
                    data_utworzenia, deadline)
            sql = """--sql
                INSERT INTO Zadania 
                VALUES( ?, 
                        (SELECT id FROM Statusy WHERE status = ?),
                        (SELECT id FROM Priorytety WHERE priorytet = ?),
                        ?,?,?,?,?,?);
                """
            c = self.bd.execute(sql, zadanie)
            return c.lastrowid
        except sqlite3.IntegrityError as e:
            if('Zadania.status' in e.args[0]):
                return f'Nie istnieje takiego statusa, jak "{status}"'
            elif("Zadania.priorytet" in e.args[0]):
                return f'Nie istnieje takiego prioryteta, jak "{priorytet}"'
            else:
                return 'Problem wewnętrzny, sorky'
        