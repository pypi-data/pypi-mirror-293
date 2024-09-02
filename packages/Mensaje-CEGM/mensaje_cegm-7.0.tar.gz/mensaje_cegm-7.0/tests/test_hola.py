
# De esta manera podemos importar un código.py entero.
#import saludos

#saludos.saludar()

#--------------------------------------------------------------
#De esta manera se puede importar únicamente una función en especifico.
#Es posible importar varias funciones de un archivo.py, separandolas por comas. como por ejemplo: from saludos import saludar, despedir
#Es posible importar todas las funciones usando * por ejemplo: from saludos import *

import unittest
import numpy as np
from Mensaje.hola.saludos import generar_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6)
        )
