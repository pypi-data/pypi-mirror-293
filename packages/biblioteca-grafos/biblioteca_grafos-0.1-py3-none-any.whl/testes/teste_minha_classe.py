# tests/test_classe_exemplo.py

import unittest
from biblioteca_grafos.grafo import Calculadora

class TestCalculadora(unittest.TestCase):
    def test_somar(self):
        calc = Calculadora()
        self.assertEqual(calc.somar(1, 2), 3)
    
    def test_subtrair(self):
        calc = Calculadora()
        self.assertEqual(calc.subtrair(5, 3), 2)

if __name__ == '__main__':
    unittest.main()
