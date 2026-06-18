import unittest
from datetime import date
from eventos import CalendarioLaboral

class TestCalendarioLaboral(unittest.TestCase):

    def test_fin_de_semana_es_no_laborable(self):
        sabado = date(2026, 1, 3)  # un sábado real
        self.assertTrue(CalendarioLaboral.es_dia_festivo(sabado))

    def test_dia_laborable_normal(self):
        lunes = date(2026, 1, 5)  # un lunes normal, sin festivo
        self.assertFalse(CalendarioLaboral.es_dia_festivo(lunes))

    def test_festivo_es_no_laborable(self):
        navidad = date(2026, 12, 25)
        self.assertTrue(CalendarioLaboral.es_dia_festivo(navidad))


if __name__ == "__main__":
    unittest.main()