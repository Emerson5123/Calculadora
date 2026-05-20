import pytest
from testtools import TestCase
from testtools.matchers import Equals, Raises, MatchesException

# Importamos la función de tu calculadora
from calculadora import calcular_precio_final

class TestCalculadoraDescuentos(TestCase):
    
    # -------------------------------------------------------------------------
    # PRUEBAS DE EXCEPCIONES (R1 y R2) usando Matchers de testtools
    # -------------------------------------------------------------------------
    
    def test_r1_descuento_limite_inferior(self):
        """R1: Validar que un descuento negativo lance ValueError con su mensaje correspondiente."""
        self.assertThat(
            lambda: calcular_precio_final(100, -5),
            Raises(MatchesException(ValueError, "El descuento debe estar entre 0 y 100."))
        )

    def test_r1_descuento_limite_superior(self):
        """R1: Validar que un descuento mayor a 100 lance ValueError."""
        self.assertThat(
            lambda: calcular_precio_final(100, 105),
            Raises(MatchesException(ValueError, "El descuento debe estar entre 0 y 100."))
        )

    def test_r2_precio_cero_lanza_error(self):
        """R2: Validar que un precio de 0 lance ValueError."""
        self.assertThat(
            lambda: calcular_precio_final(0, 20),
            Raises(MatchesException(ValueError, "El precio original debe ser un valor positivo."))
        )

    def test_r2_precio_negativo_lanza_error(self):
        """R2: Validar que un precio negativo lance ValueError."""
        self.assertThat(
            lambda: calcular_precio_final(-50, 20),
            Raises(MatchesException(ValueError, "El precio original debe ser un valor positivo."))
        )

    # -------------------------------------------------------------------------
    # PRUEBAS DE CÁLCULO Y REDONDEO (R3, R4 y R5) usando Equals de testtools
    # -------------------------------------------------------------------------

    def test_r3_r4_calculo_base_y_redondeo(self):
        """R3 y R4: Validar descuento normal y redondeo exacto a 2 decimales."""
        # 100 con 15.5% de descuento = 84.5
        self.assertThat(calcular_precio_final(100, 15.5), Equals(84.5))
        
        # Como tu función ya aplica un round(..., 2) de forma nativa,
        # Equals valida de forma exacta el número redondeado (41.39)
        self.assertThat(calcular_precio_final(45.99, 10), Equals(41.39))

    def test_r5_descuento_especial_aplicado(self):
        """R5: Validar el 5% extra sobre lo ya descontado cuando el descuento es >= 80%."""
        # Precio: 100, Descuento: 80% -> Esperado: 19.0
        self.assertThat(calcular_precio_final(100, 80), Equals(19.0))


# -------------------------------------------------------------------------
# Integración con la matriz de pruebas parametrizadas de Pytest
# -------------------------------------------------------------------------
@pytest.mark.parametrize("precio, descuento, esperado", [
    (100, 0, 100.0),    # Sin descuento
    (100, 50, 50.0),    # Mitad de precio
    (200, 90, 19.0),    # Descuento R5 correcto
])
def test_casos_exito_pytest(precio, descuento, esperado):
    assert calcular_precio_final(precio, descuento) == esperado