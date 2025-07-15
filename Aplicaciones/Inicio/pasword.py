import random

# generación de password 
def contraseña():

    minus = "abcdefghijklmnopqrstuvwxyz"
    mayus = minus.upper()
    num = "1234567890"
    simbolo = "@#$%!&/?¡¿*+-<>="

    base = minus+mayus+num+simbolo
    longitud= 12

    muestra = random.sample(base, longitud)
    pasword ="".join(muestra)
    
    return pasword

    
