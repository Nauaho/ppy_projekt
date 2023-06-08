import sqlite3

tworzenie = """
    --sql
    CREATE TABLE IF NOT EXISTS Adminy (
        login varchar(100) NOT NULL CONSTRAINT Adminy_pk PRIMARY KEY,
        CONSTRAINT Adminy_Uzytkowniccy FOREIGN KEY (login)
        REFERENCES Uzytkownicy (login)
    );

    CREATE TABLE IF NOT EXISTS Priorytety (
        id integer NOT NULL CONSTRAINT Priorytety_pk PRIMARY KEY,
        priorytet varchar(150) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Statusy (
        id integer NOT NULL CONSTRAINT Statusy_pk PRIMARY KEY,
        status varchar(150) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Uzytkownicy (
        login varchar(100) NOT NULL CONSTRAINT Uzytkownicy_pk PRIMARY KEY,
        sol varchar(10) NOT NULL,
        haslo varchar(64) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Zadnia (
        id integer NOT NULL CONSTRAINT Zadnia_pk PRIMARY KEY,
        status integer NOT NULL,
        priorytet integer NOT NULL,
        uzytkownik varchar(100) NOT NULL,
        admin varchar(100),
        CONSTRAINT Zadnia_Statusy FOREIGN KEY (status)
        REFERENCES Statusy (id),
        CONSTRAINT Zadnia_Priorytety FOREIGN KEY (priorytet)
        REFERENCES Priorytety (id),
        CONSTRAINT Zadnia_Uzytkownicy FOREIGN KEY (uzytkownik)
        REFERENCES Uzytkownicy (login)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
        CONSTRAINT Zadnia_Adminy FOREIGN KEY (admin)
        REFERENCES Adminy (login)
        ON DELETE SET NULL 
        ON UPDATE CASCADE
    );
    """

def init(name):

    bd = sqlite3.connect(name)
    bd.executescript(tworzenie)
   
    return bd