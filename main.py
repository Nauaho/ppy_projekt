from baza_danych import tworzenie, wypelnienie, hasher

bd = tworzenie.init("baza_danych\\dane\\dane.db")


print(hasher.uzytkownik_sol_i_haslo('nazar', '23423'))



