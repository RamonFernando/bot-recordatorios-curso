"""Tests del cálculo de fechas del bot."""
import unittest
from datetime import date

from bot import asistente


class TestFechas(unittest.TestCase):
    def test_a_fecha_convierte_texto_iso(self):
        self.assertEqual(asistente.a_fecha("2026-11-20"), date(2026, 11, 20))

    def test_faltan_avisa_de_hoy_y_de_manana(self):
        hoy = date(2026, 11, 3)
        self.assertEqual(asistente.faltan(hoy, hoy), "¡HOY a las 23:59!")
        self.assertEqual(asistente.faltan(hoy, date(2026, 11, 4)), "mañana")

    def test_faltan_cuenta_dias_y_detecta_vencidas(self):
        hoy = date(2026, 11, 3)
        self.assertEqual(asistente.faltan(hoy, date(2026, 11, 8)), "faltan 5 días")
        self.assertEqual(asistente.faltan(hoy, date(2026, 11, 1)), "VENCIDA hace 2 d")


if __name__ == "__main__":
    unittest.main()
