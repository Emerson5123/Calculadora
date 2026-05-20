import unittest
# Importamos la función de tu calculadora
from calculadora import calcular_precio_final

class TestCalculadoraUnittest(unittest.TestCase):
    """Suite de pruebas unitarias oficiales utilizando el framework nativo unittest."""

    # -------------------------------------------------------------------------
    # PRUEBAS DE EXCEPCIONES (R1 y R2)
    # -------------------------------------------------------------------------
    def test_r1_descuento_limite_inferior(self):
        """R1: Validar que un descuento menor a 0 lance ValueError"""
        with self.assertRaises(ValueError) as contexto:
            calcular_precio_final(100, -10)
        # Unittest permite verificar el mensaje capturado en el contexto
        self.assertEqual(str(contexto.exception), "El descuento debe estar entre 0 y 100.")

    def test_r1_descuento_limite_superior(self):
        """R1: Validar que un descuento mayor a 100 lance ValueError"""
        with self.assertRaises(ValueError) as contexto:
            calcular_precio_final(100, 120)
        self.assertEqual(str(contexto.exception), "El descuento debe estar entre 0 y 100.")

    def test_r2_precio_invalido_error(self):
        """R2: Validar que precios cero o negativos lancen ValueError"""
        with self.assertRaises(ValueError) as contexto_cero:
            calcular_precio_final(0, 15)
        self.assertEqual(str(contexto_cero.exception), "El precio original debe ser un valor positivo.")

        with self.assertRaises(ValueError) as contexto_negativo:
            calcular_precio_final(-5, 15)
        self.assertEqual(str(contexto_negativo.exception), "El precio original debe ser un valor positivo.")

    # -------------------------------------------------------------------------
    # PRUEBAS DE CÁLCULO Y REDONDEO (R3, R4 y R5)
    # -------------------------------------------------------------------------
    def test_r3_r4_calculo_base_y_redondeo(self):
        """R3 y R4: Validar descuento estándar y redondeo a dos decimales"""
        # Caso base normal (100 - 20% = 80)
        self.assertEqual(calcular_precio_final(100, 20), 80.0)
        
        # Caso con decimales para verificar el redondeo (45.99 - 10% = 41.391 -> 41.39)
        self.assertEqual(calcular_precio_final(45.99, 10), 41.39)

    def test_r5_descuento_especial_aplicado(self):
        """R5: Validar el 5% extra acumulado si el descuento es igual o mayor a 80%"""
        # Precio: 200, Descuento: 90%
        # 200 - 90% = 20 restante -> 20 - 5% = 19.0
        self.assertEqual(calcular_precio_final(200, 90), 19.0)


# Este bloque permite ejecutar este archivo directamente con "python test_unittest.py"
if __name__ == "__main__":
    unittest.main()