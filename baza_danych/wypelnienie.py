import sqlite3
from . import hasher


uzytkownicy = (
    ('admin', '1234'),    
    ('ola', '1234'),
    ('nazar', '1234')
)

adminy =(
    ('admin',),
    ('ola',)
)

priorytety = (
    (None,'nizki'),
    (None,'średni'),
    (None,'wysoki')
)

statusy = (
    (None,"do zrobienia"),
    (None,"w trakcie"),
    (None,"zakończone"),
)

def seed(bd):
    for u in uzytkownicy:
        bd.execute("INSERT INTO Uzytkownicy VALUES (?,?,?);", 
                   hasher.uzytkownik_sol_i_haslo(u[0], u[1]))
    bd.executemany("INSERT INTO Adminy VALUES (?);", adminy)
    bd.executemany("INSERT INTO Priorytety VALUES (?,?);", priorytety)
    bd.executemany("INSERT INTO Statusy VALUES (?,?);", statusy)
    bd.commit()

