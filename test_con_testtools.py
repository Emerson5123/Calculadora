from testtools import TestCase
from testtools.matchers import Equals, Raises, MatchesException
from calculadora import calcular_precio_final

class TestCalculadoraConTesttools(TestCase):
    
    def test_validacion_matematica_base(self):
        """testtools - Verifica el resultado exacto usando el Matcher Equals"""
        # La sintaxis assertThat separa el objeto bajo prueba de la condición esperada
        self.assertThat(calcular_precio_final(100, 20), Equals(80.0))
        self.assertThat(calcular_precio_final(100, 80), Equals(19.0))

    def test_blindaje_de_excepciones_y_mensajes(self):
        """testtools - Verifica que la excepción y el mensaje de texto sean exactos"""
        # testtools inspecciona que el mensaje de error de la regla R1 sea idéntico,
        # protegiendo los textos que verá el usuario final en la interfaz.
        self.assertThat(
            lambda: calcular_precio_final(100, 150),
            Raises(MatchesException(ValueError, "El descuento debe estar entre 0 y 100."))
        )
        
        # Protegemos el mensaje de la regla R2 (precio negativo)
        self.assertThat(
            lambda: calcular_precio_final(-10, 20),
            Raises(MatchesException(ValueError, "El precio original debe ser un valor positivo."))
        )
        