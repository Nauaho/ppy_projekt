import sqlite3
import BazaDanych

uzytkownicy = (
    ('admin', '1234'),    
    ('ola', '1234'),
    ('nazar', '1234')
)

adminy =(
    ('admin'),
    ('ola')
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
    
    bd.executemany("INSERT INTO Uzytkownicy VALUES (?,?,?);", uzytkownicy)
    bd.executemany("INSERT INTO Adminy VALUES (?);", adminy)
    bd.executemany("INSERT INTO Priorytety VALUES (?,?);", priorytety)
    bd.executemany("INSERT INTO Statusy VALUES (?,?);", statusy)

