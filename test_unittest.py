import unittest
from unittest.mock import patch, mock_open
import os

# Importamos las funciones desde nuestro archivo de lógica
from calculadora import calcular_precio_final, registrar_en_auditoria

class TestCalculadoraDescuentos(unittest.TestCase):

    # --- PRUEBAS PARA calcular_precio_final ---

    def test_descuento_estandar(self):
        """Caso Feliz (R3 y R4): Descuento estándar y redondeo correcto"""
        # 100 - 20% = 80
        self.assertEqual(calcular_precio_final(100, 20), 80.0)
        # Prueba de redondeo a 2 decimales: 55.55 * (1 - 0.125) = 48.60625 -> 48.61
        self.assertEqual(calcular_precio_final(55.55, 12.5), 48.61)

    def test_descuento_acumulado_limite(self):
        """Regla R5: Descuentos mayores o iguales al 80% aplican el 5% extra"""
        # Exactamente 80%: 100 - 80% = 20. Luego 20 * 0.95 = 19.0
        self.assertEqual(calcular_precio_final(100, 80), 19.0)
        # Mayor al 80% (90%): 100 - 90% = 10. Luego 10 * 0.95 = 9.5
        self.assertEqual(calcular_precio_final(100, 90), 9.5)

    def test_error_descuento_fuera_de_rango(self):
        """Regla R1: Error si el descuento no está entre 0 y 100"""
        with self.assertRaises(ValueError) as context:
            calcular_precio_final(100, -1)
        self.assertEqual(str(context.exception), "El descuento debe estar entre 0 y 100.")

        with self.assertRaises(ValueError) as context:
            calcular_precio_final(100, 101)
        self.assertEqual(str(context.exception), "El descuento debe estar entre 0 y 100.")

    def test_error_precio_no_positivo(self):
        """Regla R2: Error si el precio original es menor o igual a cero"""
        with self.assertRaises(ValueError) as context:
            calcular_precio_final(0, 10)
        self.assertEqual(str(context.exception), "El precio original debe ser un valor positivo.")

        with self.assertRaises(ValueError) as context:
            calcular_precio_final(-50, 10)
        self.assertEqual(str(context.exception), "El precio original debe ser un valor positivo.")


    # --- PRUEBAS PARA registrar_en_auditoria ---

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_auditoria_registro_exitoso_archivo_nuevo(self, mock_file, mock_exists):
        """Verifica el flujo cuando la auditoría es exitosa y el archivo no existe todavía"""
        mock_exists.return_value = False  # Simulamos que el archivo NO existe
        
        registrar_en_auditoria(100, 20, 80.0, es_exitoso=True)
        
        # Verificamos que abrió el archivo para escribir el encabezado ('w') y luego añadir ('a')
        mock_file.assert_any_call("auditoria.txt", "w", encoding="utf-8")
        mock_file.assert_any_call("auditoria.txt", "a", encoding="utf-8")
        
        # Verificamos que se escribió la estructura del log correctamente
        manejador_archivo = mock_file()
        manejador_archivo.write.assert_any_call("=== HISTORIAL DE AUDITORÍA DE LA CALCULADORA ===\n\n")
        manejador_archivo.write.assert_any_call("ENTRADA -> Precio: 100, Descuento: 20% | RESULTADO: $80.0\n")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_auditoria_registro_fallido_archivo_existente(self, mock_file, mock_exists):
        """Verifica el flujo cuando ocurre un error y el archivo ya existía"""
        mock_exists.return_value = True  # Simulamos que el archivo SÍ existe
        
        mensaje_error = "Debe ingresar valores numéricos válidos."
        registrar_en_auditoria("abc", 10, mensaje_error, es_exitoso=False)
        
        # Al existir el archivo, no debería intentar abrirlo en modo escritura 'w'
        for llamada in mock_file.call_args_list:
            self.assertNotEqual(llamada[0][1], "w")
            
        # Debe abrir solo en modo append 'a'
        mock_file.assert_called_once_with("auditoria.txt", "a", encoding="utf-8")
        
        # Verificamos el formato del string de error en el log
        manejador_archivo = mock_file()
        manejador_archivo.write.assert_called_once_with(
            f"ENTRADA -> Precio: abc, Descuento: 10% | ERROR: {mensaje_error}\n"
        )

if __name__ == "__main__":
    unittest.main()