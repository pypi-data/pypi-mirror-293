import numpy as np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una prueba de la nueva versión 7.0")

def generar_array(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__(self):
        print("Hola, te saludo desde Saludo.__init__()")


# Esto es para que no se ejecute el código si se importa, únicamente en saludos.py
if __name__ == "__main__":
   print(generar_array(5))