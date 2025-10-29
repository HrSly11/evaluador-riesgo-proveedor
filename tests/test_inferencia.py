"""
Tests de inferencia correcta
Valida que las reglas se disparen correctamente según los datos ingresados
"""

import pytest
from engine import evaluar_proveedor


def test_proveedor_bajo_riesgo():
    """
    Test 1: Verificar que un proveedor excelente resulte en BAJO riesgo
    """
    datos_proveedor_excelente = {
        'liquidez_corriente': 2.5,
        'endeudamiento': 30,
        'rentabilidad': 18,
        'anos_operacion': 15,
        'cumplimiento_entregas': 98,
        'capacidad_produccion': 20000,
        'demanda_estimada': 12000,
        'certificaciones_calidad': ['ISO 9001', 'ISO 14001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 4.8,
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_proveedor_excelente)
    
    # Assertions
    assert resultado['nivel_riesgo'] == 'BAJO', \
        f"Se esperaba riesgo BAJO pero se obtuvo {resultado['nivel_riesgo']}"
    
    assert resultado['puntaje_total'] <= 0, \
        f"Se esperaba puntaje <= 0 pero se obtuvo {resultado['puntaje_total']}"
    
    # Verificar que se activaron reglas positivas
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    assert 'liquidez_excelente' in reglas_activadas, \
        "Debería activarse la regla de liquidez excelente"
    
    assert 'cumplimiento_excelente' in reglas_activadas, \
        "Debería activarse la regla de cumplimiento excelente"
    
    assert resultado['total_reglas'] > 0, \
        "Deben haberse activado al menos una regla"
    
    print(f"✓ Test passed: Proveedor excelente correctamente clasificado como {resultado['nivel_riesgo']}")
    print(f"  Puntaje: {resultado['puntaje_total']}")
    print(f"  Reglas activadas: {resultado['total_reglas']}")


def test_proveedor_alto_riesgo():
    """
    Test 2: Verificar que un proveedor con problemas graves resulte en ALTO o CRÍTICO riesgo
    """
    datos_proveedor_riesgoso = {
        'liquidez_corriente': 0.6,
        'endeudamiento': 85,
        'rentabilidad': -5,
        'anos_operacion': 1,
        'cumplimiento_entregas': 70,
        'capacidad_produccion': 5000,
        'demanda_estimada': 8000,
        'certificaciones_calidad': [],
        'licencias_vigentes': False,
        'certificado_tributario': False,
        'cumplimiento_laboral': False,
        'demandas_legales': 4,
        'calificacion_mercado': 2.5,
        'incidentes_seguridad': 3,
        'practicas_eticas': False,
        'responsabilidad_ambiental': False
    }
    
    resultado = evaluar_proveedor(datos_proveedor_riesgoso)
    
    # Assertions
    assert resultado['nivel_riesgo'] in ['ALTO', 'CRÍTICO'], \
        f"Se esperaba riesgo ALTO o CRÍTICO pero se obtuvo {resultado['nivel_riesgo']}"
    
    assert resultado['puntaje_total'] > 30, \
        f"Se esperaba puntaje > 30 pero se obtuvo {resultado['puntaje_total']}"
    
    # Verificar que se activaron reglas de riesgo
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    assert 'liquidez_riesgosa' in reglas_activadas, \
        "Debería activarse la regla de liquidez riesgosa"
    
    assert 'licencias_vencidas' in reglas_activadas, \
        "Debería activarse la regla de licencias vencidas"
    
    assert 'crisis_financiera' in reglas_activadas, \
        "Debería activarse la regla de crisis financiera (liquidez + endeudamiento)"
    
    print(f"✓ Test passed: Proveedor riesgoso correctamente clasificado como {resultado['nivel_riesgo']}")
    print(f"  Puntaje: {resultado['puntaje_total']}")
    print(f"  Reglas de riesgo activadas: {len([r for r in resultado['reglas_activadas'] if r['impacto'] > 0])}")


def test_proveedor_moderado():
    """
    Test 3: Verificar que un proveedor con indicadores mixtos resulte en MODERADO
    """
    datos_proveedor_moderado = {
        'liquidez_corriente': 1.3,
        'endeudamiento': 55,
        'rentabilidad': 8,
        'anos_operacion': 5,
        'cumplimiento_entregas': 88,
        'capacidad_produccion': 10000,
        'demanda_estimada': 9500,
        'certificaciones_calidad': ['ISO 9001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 1,
        'calificacion_mercado': 3.8,
        'incidentes_seguridad': 1,
        'practicas_eticas': True,
        'responsabilidad_ambiental': False
    }
    
    resultado = evaluar_proveedor(datos_proveedor_moderado)
    
    # Assertions
    assert resultado['nivel_riesgo'] in ['BAJO', 'MODERADO'], \
        f"Se esperaba riesgo BAJO o MODERADO pero se obtuvo {resultado['nivel_riesgo']}"
    
    assert resultado['puntaje_total'] <= 30, \
        f"Se esperaba puntaje <= 30 pero se obtuvo {resultado['puntaje_total']}"
    
    # Verificar que hay un mix de reglas positivas y negativas
    impactos = [r['impacto'] for r in resultado['reglas_activadas']]
    tiene_positivos = any(i > 0 for i in impactos)
    tiene_negativos = any(i < 0 for i in impactos)
    
    assert tiene_positivos and tiene_negativos, \
        "Debería haber tanto reglas que aumentan como reducen el riesgo"
    
    print(f"✓ Test passed: Proveedor moderado correctamente clasificado como {resultado['nivel_riesgo']}")
    print(f"  Puntaje: {resultado['puntaje_total']}")
    print(f"  Reglas positivas: {len([i for i in impactos if i < 0])}")
    print(f"  Reglas negativas: {len([i for i in impactos if i > 0])}")


def test_regla_crisis_financiera():
    """
    Test 4: Verificar que la regla compuesta de crisis financiera se active correctamente
    """
    datos_crisis = {
        'liquidez_corriente': 0.7,  # < 1.0
        'endeudamiento': 75,  # > 70
        'rentabilidad': 5,
        'anos_operacion': 10,
        'cumplimiento_entregas': 95,
        'capacidad_produccion': 15000,
        'demanda_estimada': 10000,
        'certificaciones_calidad': ['ISO 9001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 4.0,
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_crisis)
    
    # Verificar que la regla de crisis financiera se activó
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    assert 'crisis_financiera' in reglas_activadas, \
        "Debería activarse la regla de crisis financiera cuando liquidez < 1.0 Y endeudamiento > 70"
    
    # Verificar que también se activaron las reglas individuales
    assert 'liquidez_riesgosa' in reglas_activadas
    assert 'endeudamiento_alto' in reglas_activadas
    
    print("✓ Test passed: Regla compuesta de crisis financiera se activa correctamente")
    print(f"  Reglas financieras activadas: {[r for r in reglas_activadas if 'liquidez' in r or 'endeudamiento' in r or 'crisis' in r]}")


def test_capacidad_insuficiente():
    """
    Test 5: Verificar que se detecte capacidad de producción insuficiente
    """
    datos_capacidad_baja = {
        'liquidez_corriente': 2.0,
        'endeudamiento': 35,
        'rentabilidad': 12,
        'anos_operacion': 8,
        'cumplimiento_entregas': 92,
        'capacidad_produccion': 5000,  # Menor que demanda
        'demanda_estimada': 8000,  # Mayor que capacidad
        'certificaciones_calidad': ['ISO 9001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 4.2,
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_capacidad_baja)
    
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    assert 'capacidad_insuficiente' in reglas_activadas, \
        "Debería activarse la regla de capacidad insuficiente cuando capacidad < demanda"
    
    # Buscar el impacto de esta regla específica
    regla_capacidad = next((r for r in resultado['reglas_activadas'] if r['regla'] == 'capacidad_insuficiente'), None)
    
    assert regla_capacidad is not None
    assert regla_capacidad['impacto'] > 0, "Capacidad insuficiente debe aumentar el riesgo"
    
    print("✓ Test passed: Detección de capacidad insuficiente funciona correctamente")
    print(f"  Capacidad: {datos_capacidad_baja['capacidad_produccion']} vs Demanda: {datos_capacidad_baja['demanda_estimada']}")


if __name__ == "__main__":
    # Ejecutar tests individualmente para debugging
    print("=" * 80)
    print("EJECUTANDO TESTS DE INFERENCIA")
    print("=" * 80)
    print()
    
    test_proveedor_bajo_riesgo()
    print()
    test_proveedor_alto_riesgo()
    print()
    test_proveedor_moderado()
    print()
    test_regla_crisis_financiera()
    print()
    test_capacidad_insuficiente()
    print()
    
    print("=" * 80)
    print("✓ TODOS LOS TESTS DE INFERENCIA PASARON EXITOSAMENTE")
    print("=" * 80)