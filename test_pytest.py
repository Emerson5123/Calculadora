import pytest
# Importamos la función de tu calculadora
from calculadora import calcular_precio_final

# -------------------------------------------------------------------------
# PRUEBAS DE EXCEPCIONES (R1 y R2) usando pytest.raises
# -------------------------------------------------------------------------

def test_r1_descuento_limite_inferior():
    """R1: Validar que un descuento menor a 0 lance ValueError y su mensaje exacto."""
    with pytest.raises(ValueError) as info_error:
        calcular_precio_final(100, -15)
    # Pytest guarda la excepción en info_error.value
    assert str(info_error.value) == "El descuento debe estar entre 0 y 100."


def test_r1_descuento_limite_superior():
    """R1: Validar que un descuento mayor a 100 lance ValueError."""
    with pytest.raises(ValueError) as info_error:
        calcular_precio_final(100, 110)
    assert str(info_error.value) == "El descuento debe estar entre 0 y 100."


def test_r2_precio_invalido_error():
    """R2: Validar que precios de cero o negativos lancen el error correspondiente."""
    with pytest.raises(ValueError) as info_cero:
        calcular_precio_final(0, 50)
    assert str(info_cero.value) == "El precio original debe ser un valor positivo."

    with pytest.raises(ValueError) as info_negativo:
        calcular_precio_final(-25, 50)
    assert str(info_negativo.value) == "El precio original debe ser un valor positivo."


# -------------------------------------------------------------------------
# MATRIZ DE PRUEBAS PARAMETRIZADAS (R3, R4 y R5)
# Esto es una característica estrella de Pytest: una sola función prueba 4 escenarios
# -------------------------------------------------------------------------
@pytest.mark.parametrize("precio, descuento, esperado", [
    (100.0, 20.0, 80.0),    # R3: Caso base normal (100 - 20% = 80)
    (45.99, 10.0, 41.39),   # R4: Verificación de redondeo exacto a 2 decimales
    (100.0, 80.0, 19.0),    # R5: Descuento especial límite inferior (100 - 80% = 20 -> 20 - 5% = 19)
    (200.0, 90.0, 19.0),    # R5: Descuento especial con precio mayor (200 - 90% = 20 -> 20 - 5% = 19)
])
def test_regresion_calculos_exitosos(precio, descuento, esperado):
    """Prueba de regresión automatizada para todos los flujos matemáticos correctos."""
    assert calcular_precio_final(precio, descuento) == esperado