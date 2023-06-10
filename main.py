from baza_danych.BazaDanych import BazaDanych

path = "baza_danych\\dane\\dane.db"

db = BazaDanych(path)

# result = db.zaloguj_sie(input('Login: '), input('Haslo: '));
result = db.zaloguj_sie('nazar', '1234')
print(result)


