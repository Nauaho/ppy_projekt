import sqlite3
import datetime
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

zadania = (
    ( None, 1, 1, 'nazar', 'ola', 'Backend', 'Zrób zwykły backend z wygodnym interfacem, albo zabiję',datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=1)),
    ( None, 2, 2, 'ola', 'admin', 'Frontend', 'Zrób zwykły frontend z wygodnym GUI :3 ',datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(weeks=1)),
    ( None, 3, 1, 'nazar', 'admin', 'Kup Plecak', 'Kup Plecak zrobiony ze złota',datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=2)),
    ( None, 2, 3, 'nazar', None, 'Sprobować sushi', 'Chcę sushi',datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=1)),
    ( None, 3, 2, 'admin', None, 'Kupić nową koszulkę', 'Kupić fajną koszulkę z Pink Floyd',datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(weeks=4)))

def seed(bd):
    # check = "SELECT Count(*) FROM Zadania;"
    # cursor = bd.execute(check)
    # if( int(cursor.fetchall()[0]) > 0 ):
    #     bd.commit()
    #     cursor.close()
    #     return
    for u in uzytkownicy:
        bd.execute("INSERT INTO Uzytkownicy VALUES (?,?,?);", 
                   hasher.uzytkownik_sol_i_haslo(u[0], u[1]))
    bd.executemany("INSERT INTO Adminy VALUES (?);", adminy)
    bd.executemany("INSERT INTO Priorytety VALUES (?,?);", priorytety)
    bd.executemany("INSERT INTO Statusy VALUES (?,?);", statusy)
    bd.executemany("INSERT INTO Zadania VALUES (?,?,?,?,?,?,?,?,?);",zadania)
    bd.commit()

