import pytest
from calculadora import calcular_precio_final

# =========================================================================
# FLUJO TDD: Primero pensamos en los requisitos y los escribimos en código
# =========================================================================

def test_requisito_descuento_normal():
    """TDD - Paso 1: Diseñar el caso base exitoso"""
    # Pensamos: 'Si entran 100 con 20% de descuento, debe retornar 80.0'
    resultado = calcular_precio_final(100, 20)
    assert resultado == 80.0


def test_requisito_error_descuento_excedido():
    """TDD - Paso 2: Diseñar el comportamiento ante errores"""
    # Pensamos: 'Si alguien pone un descuento de 150, el sistema debe lanzar un ValueError'
    with pytest.raises(ValueError):
        calcular_precio_final(100, 150)


def test_requisito_descuento_super_promocion():
    """TDD - Paso 3: Diseñar las reglas especiales (R5)"""
    # Pensamos: 'Si el descuento es del 80%, debe aplicar el 5% extra sobre el remanente (20)'
    # 20 * 0.95 = 19.0
    assert calcular_precio_final(100, 80) == 19.0