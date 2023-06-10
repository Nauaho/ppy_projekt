import hashlib
import random
import string

def uzytkownik_sol_i_haslo(login, haslo):
    sol = __daj_mi_sol()
    material = sol.join(haslo).encode()
    return (login, sol, hashlib.sha256(material).hexdigest())

def __daj_mi_sol():
    solka = ""
    for i in range(10):
        solka += random.choice(string.ascii_letters)
    return solka

def weryfikuj_haslo(sol, haslo, haslo_haszowane):
    material = sol.join(haslo).encode()
    return hashlib.sha256(material).hexdigest() == haslo_haszowane;