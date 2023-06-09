from . import hasher 
import sqlite3

class BazaDanych:

    def __init__(self, bd):
        self.bd = bd
    
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
        sol = uzytkownik[0]['sol']
        login = uzytkownik[0]['login']
        haslo_haszowane = sol = uzytkownik[0]['haslo']
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