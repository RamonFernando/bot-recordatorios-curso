"""Tests de todas_las_entregas: entregas definidas más las previstas de cada lliurament.

Son tests de caracterización: fijan el comportamiento actual del bot con
datos mínimos escritos aquí, sin leer ningún archivo del repositorio.
"""
import copy
import unittest
from unittest import mock

from bot import asistente


def build_data():
    """Devuelve un diccionario de datos nuevo en cada llamada.

    Los lliuraments van en orden inverso para que el orden del resultado
    dependa de la función y no de los datos.
    """
    return {
        "lliuraments": [
            {"n": 2, "inicio": "2026-12-01", "fin": "2026-12-21",
             "temas": {"CE_5071": "Tema L2 de 5071"}},
            {"n": 1, "inicio": "2026-11-02", "fin": "2026-11-30",
             "temas": {"CE_5071": "Tema L1 de 5071", "CE_5073": "Tema L1 de 5073"}},
        ],
        "entregas": [
            {"id": "L1-5073-tarea", "lliurament": 1, "modulo": "CE_5073",
             "tipo": "tarea", "titulo": "Tarea de prueba", "formato": "PDF",
             "fecha": "2026-11-23", "confirmada": True},
        ],
    }


class TestTodasLasEntregas(unittest.TestCase):
    def test_defined_pair_has_no_planned_entries(self):
        """Un par (lliurament, módulo) con entrega definida no recibe previstas."""
        self.assertIn(
            "CE_5073", asistente.MODULOS_EVALUABLES,
            "CE_5073 ya no está en MODULOS_EVALUABLES: hay que adaptar los datos de prueba",
        )
        resultado = asistente.todas_las_entregas(build_data())
        del_par = [e for e in resultado if e["lliurament"] == 1 and e["modulo"] == "CE_5073"]
        self.assertEqual(len(del_par), 1, "Debe haber exactamente 1 entrada para (1, CE_5073)")
        self.assertTrue(del_par[0]["confirmada"], "La entrada de (1, CE_5073) debe ser la definida")
        self.assertEqual(del_par[0]["id"], "L1-5073-tarea")
        previstas = [e for e in del_par if not e["confirmada"]]
        self.assertEqual(previstas, [], "No debe haber previstas para (1, CE_5073)")

    def test_two_planned_entries_per_pair_without_detail(self):
        """Cada par sin entrega definida recibe una tarea y un cuestionario previstos."""
        resultado = asistente.todas_las_entregas(build_data())
        for n in (1, 2):
            for modulo in asistente.MODULOS_EVALUABLES:
                if (n, modulo) == (1, "CE_5073"):
                    continue
                with self.subTest(lliurament=n, modulo=modulo):
                    previstas = [e for e in resultado
                                 if e["lliurament"] == n and e["modulo"] == modulo
                                 and not e["confirmada"]]
                    self.assertEqual(len(previstas), 2,
                                     f"El par ({n}, {modulo}) debe tener 2 previstas")
                    self.assertEqual({e["tipo"] for e in previstas}, {"tarea", "cuestionario"},
                                     f"El par ({n}, {modulo}) debe tener tarea y cuestionario")
        # 2 lliuraments x módulos x 2 previstas, menos las 2 del par definido, más la definida.
        total_esperado = 2 * len(asistente.MODULOS_EVALUABLES) * 2 - 2 + 1
        self.assertEqual(len(resultado), total_esperado,
                         "El total de entregas no coincide con el esperado")

    def test_planned_entries_fields(self):
        """Cada prevista lleva formato, fecha de fin del lliurament e id con el patrón del bot."""
        datos = build_data()
        fin_por_lliurament = {ll["n"]: ll["fin"] for ll in datos["lliuraments"]}
        resultado = asistente.todas_las_entregas(datos)
        previstas = [e for e in resultado if not e["confirmada"]]
        for e in previstas:
            with self.subTest(id=e["id"]):
                self.assertEqual(e["formato"], "por confirmar",
                                 "Una prevista debe tener formato 'por confirmar'")
                self.assertEqual(e["fecha"], fin_por_lliurament[e["lliurament"]],
                                 "Una prevista debe vencer el día de fin de su lliurament")
                sufijo = "tarea" if e["tipo"] == "tarea" else "quiz"
                self.assertEqual(e["id"], f"L{e['lliurament']}-{e['modulo'][3:]}-{sufijo}",
                                 "El id de la prevista no sigue el patrón esperado")
        ids_previstas = {e["id"] for e in previstas}
        for id_esperado in ("L1-5072-quiz","L1-5071-tarea", "L2-5073-tarea"):
            with self.subTest(id_esperado=id_esperado):
                self.assertIn(id_esperado, ids_previstas,
                              f"Falta la prevista {id_esperado}")

    def test_result_is_sorted_by_date_module_and_type(self):
        """El resultado sale ordenado por fecha, módulo y tipo."""
        resultado = asistente.todas_las_entregas(build_data())
        claves = [(e["fecha"], e["modulo"], e["tipo"]) for e in resultado]
        self.assertEqual(claves, sorted(claves),
                         "El resultado no está ordenado por (fecha, modulo, tipo)")
        self.assertEqual(resultado[0]["id"], "L1-5073-tarea",
                         "La primera entrega debe ser la definida del 2026-11-23")
        ids = [e["id"] for e in resultado]
        self.assertLess(ids.index("L1-5071-quiz"), ids.index("L1-5071-tarea"),
                        "En el mismo módulo y fecha, el cuestionario debe ir antes que la tarea")

    def test_input_data_is_not_modified(self):
        """La función no modifica los datos de entrada y devuelve una lista nueva."""
        datos = build_data()
        copia = copy.deepcopy(datos)
        resultado = asistente.todas_las_entregas(datos)
        self.assertEqual(datos, copia, "La función ha modificado los datos de entrada")
        self.assertIsNot(resultado, datos["entregas"],
                         "La lista devuelta no debe ser la misma que datos['entregas']")

    def test_does_not_touch_files(self):
        """La función trabaja solo en memoria: no abre ningún archivo."""
        datos = build_data()
        aviso = AssertionError("todas_las_entregas no debe abrir archivos")
        with mock.patch("builtins.open", side_effect=aviso):
            resultado = asistente.todas_las_entregas(datos)
        self.assertTrue(resultado, "La función debe devolver entregas sin tocar disco")


if __name__ == "__main__":
    unittest.main()
