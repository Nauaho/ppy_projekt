from baza_danych import hasher, tworzenie
import sqlite3
import datetime
import collections

ZadanieKratka = collections.namedtuple("Zadanie", ["id","status","priorytet","admin",
                                                 "tytul","opis","data_utworzenia","deadline"])
class Zadanie:
    def __init__(self, zadanie_w_kratce):
        self.id = zadanie_w_kratce.id
        self.status = zadanie_w_kratce.status
        self.priorytet = zadanie_w_kratce.priorytet
        self.admin = zadanie_w_kratce.admin
        self.tytul = zadanie_w_kratce.tytul
        self.opis = zadanie_w_kratce.opis
        self.data_utworzenia = datetime.datetime.strptime(zadanie_w_kratce.data_utworzenia, "%Y-%m-%d %H:%M:%S.%f")
        self.deadline = datetime.datetime.strptime(zadanie_w_kratce.deadline, "%Y-%m-%d %H:%M:%S.%f")


class BazaDanych:

    def __init__(self, path):
        self.bd = tworzenie.init(path)
    
    def zarejestruj_sie(self, login, haslo):
        uzytkownik = self.__uzytkownik_o_takim_loginie(login)
        if(uzytkownik != None):
            return None
        sql = "INSERT INTO Uzytkownicy VALUES(?,?,?);"
        self.bd.execute(sql, hasher.uzytkownik_sol_i_haslo(login, haslo))
        self.bd.commit()
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
        sql = "SELECT * FROM Uzytkownicy WHERE [login] = ?;" 
        login = (login,)
        cursor = self.bd.cursor()
        cursor.execute(sql, login)
        user = cursor.fetchall()
        cursor.close()
        self.bd.commit()
        if(len(user) == 0):
            return None
        else:
            return user[0]
        
    def admin_o_takim_loginie(self, login):
        sql = "SELECT * FROM Adminy WHERE [login] = ?;"
        login = (login,)
        cursor = self.bd.cursor()
        cursor.execute(sql, login)
        admin = cursor.fetchall()
        self.bd.commit()
        cursor.close()
        if(len(admin) == 0):
            return None
        else:
            return admin[0][0]
    
    def dodaj_admina(self, login, login_nowego_admina):
        if(login != self.admin_o_takim_loginie(login)):
            return "Nie masz uprawnień do dodawania nowych adminów: nie jesteś adminem"
        if(login_nowego_admina != self.__uzytkownik_o_takim_loginie(login_nowego_admina)[0]):
            return f"Nie istenieje użytkownika o loginie '{login_nowego_admina}'"
        if(self.admin_o_takim_loginie(login_nowego_admina) == login_nowego_admina):
            return f"Użytkownik '{login_nowego_admina}' już ma uprawnienia admina"
        sql = "INSERT INTO Adminy VALUES (?);"
        c = self.bd.execute(sql,(login_nowego_admina,))
        self.bd.commit()
        c.close()
        if(c.rowcount == 1):
            return f"Użutkownik '{login_nowego_admina}' został adminem"
        else:
            self.bd.rollback()
            return f"Węwnętrzny problem, użutkownik '{login_nowego_admina}' nie został adminem"

    def usun_zadanie(self,id):
        sql = "DELETE FROM Zadania WHERE id = ?;"
        id = (id,)
        c = self.bd.execute(sql, id)
        self.bd.commit()
        c.close()
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
            self.bd.commit()
            c.close()
            return c.lastrowid
        except sqlite3.IntegrityError as e:
            self.bd.rollback()
            if('Zadania.status' in e.args[0]):
                return f'Nie istnieje takiego statusa, jak "{status}"'
            elif("Zadania.priorytet" in e.args[0]):
                return f'Nie istnieje takiego prioryteta, jak "{priorytet}"'
            elif("Zadania.data_utworzenia" in e.args[0]):
                return f'Nie poprawny format czasu w dacie utworzenia: "{zadanie.data_utworzenia}"'
            elif("Zadania.deadline" in e.args[0]):
                return f'Nie poprawny format czasu w końcowym terminie: "{zadanie.deadline}"'
            else:
                return 'Problem wewnętrzny, sorky'
        except:
            self.bd.rollback()
            return 'Problem wewnętrzny, sorky'
    
    def daj_zadania(self, login, sortowanie = lambda a,b: True if(a.tytul>=b.tytul) else False,predykat = None ):
        sql = """--sql 
            SELECT z.id, s.status, p.priorytet, z.admin, z.tytul, z.opis, z.data_utworzenia, z.deadline
            FROM Zadania z 
                INNER JOIN Priorytety p ON p.id = z.priorytet
                INNER JOIN Statusy s ON s.id = z.status
            WHERE z.uzytkownik = ?;"""
        cursor = self.bd.cursor()
        cursor.execute(sql, (login,))
        zadania = [Zadanie(t) for t in list(map(ZadanieKratka._make, cursor.fetchall()))]
        zadania = list(filter(predykat, zadania))
        for i in range(0, len(zadania)-1):
            for j in range(0, len(zadania)-1):
                if(sortowanie(zadania[j], zadania[j+1])):
                    a = zadania[j]
                    zadania[j] = zadania[j + 1]
                    zadania[j + 1] = a
        self.bd.commit()
        cursor.close()
        return zadania

    def edytuj_zadanie(self, zadanie):
        try:
            sql = """
            UPDATE Zadania 
            SET [status] = (SELECT id FROM Statusy WHERE status = ?),
                [priorytet] = (SELECT id FROM Priorytety WHERE priorytet = ?),
                [admin] = ?,
                tytul = ?,
                opis = ?,
                data_utworzenia = ?,
                deadline = ?
            WHERE id = ?
            ;"""
            zadanie_kratka = (zadanie.status,
                            zadanie.priorytet,
                            zadanie.admin,
                            zadanie.tytul,
                            zadanie.opis,
                            zadanie.data_utworzenia,
                            zadanie.deadline,
                            zadanie.id)
            c = self.bd.execute(sql, zadanie_kratka)
            self.bd.commit()
            c.close()
            if(c.rowcount == 1 ):
                return f"Zadanie nr {zadanie.id} zostało zmienione, {c.rowcount}"
            else:
                self.bd.rollback()
                return f"Zadanie nr {zadanie.id} nie udało się zmienić, {c.rowcount}"
        except sqlite3.IntegrityError as e:
            self.bd.rollback()
            if('Zadania.status' in e.args[0]):
                return f'Nie istnieje takiego statusa, jak "{zadanie.status}"'
            elif("Zadania.priorytet" in e.args[0]):
                return f'Nie istnieje takiego prioryteta, jak "{zadanie.priorytet}"'
            elif("Zadania.admin" in e.args[0]):
                return f'Nie istnieje takiego admina, jak "{zadanie.admin}"'
            elif("Zadania.data_utworzenia" in e.args[0]):
                return f'Nie poprawny format czasu w dacie utworzenia: "{zadanie.data_utworzenia}"'
            elif("Zadania.deadline" in e.args[0]):
                return f'Nie poprawny format czasu w końcowym terminie: "{zadanie.deadline}"'
            else:
                return 'Problem wewnętrzny, sorky'
        except:
            self.bd.rollback()
            return 'Problem wewnętrzny, sorky'