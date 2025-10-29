"""
Tests de casos borde
Valida el comportamiento del sistema en situaciones límite
"""

import pytest
from engine import evaluar_proveedor


def test_valores_exactos_en_umbrales():
    """
    Test 1: Verificar comportamiento en umbrales exactos (liquidez = 1.0, endeudamiento = 70, etc.)
    """
    datos_umbrales = {
        'liquidez_corriente': 1.0,  # Exactamente en el límite
        'endeudamiento': 70,  # Exactamente en el límite
        'rentabilidad': 0,  # Justo en cero
        'anos_operacion': 2,  # Justo en el límite de nuevo
        'cumplimiento_entregas': 80,  # Exactamente en el límite
        'capacidad_produccion': 10000,
        'demanda_estimada': 10000,  # Exactamente igual
        'certificaciones_calidad': ['ISO 9001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 3.0,  # Exactamente en el umbral
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_umbrales)
    
    # Verificar que el sistema no falla con valores en umbrales
    assert resultado is not None, "El sistema debe manejar valores en umbrales"
    assert 'nivel_riesgo' in resultado, "Debe retornar un nivel de riesgo"
    assert resultado['nivel_riesgo'] in ['BAJO', 'MODERADO', 'ALTO', 'CRÍTICO']
    
    # Verificar que se activaron algunas reglas
    assert resultado['total_reglas'] > 0, "Deben activarse reglas incluso en valores límite"
    
    print("✓ Test passed: Sistema maneja correctamente valores en umbrales exactos")
    print(f"  Nivel de riesgo: {resultado['nivel_riesgo']}")
    print(f"  Puntaje: {resultado['puntaje_total']}")


def test_valores_extremos_altos():
    """
    Test 2: Verificar comportamiento con valores extremadamente altos
    """
    datos_extremos_altos = {
        'liquidez_corriente': 10.0,  # Muy alto
        'endeudamiento': 5,  # Muy bajo
        'rentabilidad': 100,  # Extremadamente alto
        'anos_operacion': 100,  # Centenario
        'cumplimiento_entregas': 100,  # Perfecto
        'capacidad_produccion': 1000000,  # Enorme
        'demanda_estimada': 100,  # Muy pequeña comparada
        'certificaciones_calidad': ['ISO 9001', 'ISO 14001', 'OHSAS 18001', 'HACCP', 'BRC'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 5.0,  # Máximo
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_extremos_altos)
    
    # Con valores tan buenos, debe ser BAJO riesgo
    assert resultado['nivel_riesgo'] == 'BAJO', \
        f"Con valores extremadamente buenos debería ser BAJO, pero es {resultado['nivel_riesgo']}"
    
    assert resultado['puntaje_total'] < 0, \
        "Con valores extremadamente buenos el puntaje debe ser negativo"
    
    print("✓ Test passed: Sistema maneja correctamente valores extremadamente altos/buenos")
    print(f"  Puntaje: {resultado['puntaje_total']}")


def test_valores_extremos_bajos():
    """
    Test 3: Verificar comportamiento con valores extremadamente bajos/malos
    """
    datos_extremos_bajos = {
        'liquidez_corriente': 0.1,  # Casi en quiebra
        'endeudamiento': 100,  # Completamente endeudado
        'rentabilidad': -50,  # Pérdidas masivas
        'anos_operacion': 0,  # Recién creado
        'cumplimiento_entregas': 0,  # Nunca cumple
        'capacidad_produccion': 100,  # Muy pequeña
        'demanda_estimada': 100000,  # Mucho mayor que capacidad
        'certificaciones_calidad': [],  # Sin certificaciones
        'licencias_vigentes': False,
        'certificado_tributario': False,
        'cumplimiento_laboral': False,
        'demandas_legales': 50,  # Muchas demandas
        'calificacion_mercado': 1.0,  # Pésima reputación
        'incidentes_seguridad': 20,  # Muchos incidentes
        'practicas_eticas': False,
        'responsabilidad_ambiental': False
    }
    
    resultado = evaluar_proveedor(datos_extremos_bajos)
    
    # Con valores tan malos, debe ser CRÍTICO
    assert resultado['nivel_riesgo'] == 'CRÍTICO', \
        f"Con valores extremadamente malos debería ser CRÍTICO, pero es {resultado['nivel_riesgo']}"
    
    assert resultado['puntaje_total'] > 60, \
        f"Con valores extremadamente malos el puntaje debe ser > 60, pero es {resultado['puntaje_total']}"
    
    # Verificar que se activaron muchas reglas de riesgo
    reglas_riesgo = [r for r in resultado['reglas_activadas'] if r['impacto'] > 0]
    assert len(reglas_riesgo) >= 10, \
        f"Deberían activarse muchas reglas de riesgo, pero solo se activaron {len(reglas_riesgo)}"
    
    print("✓ Test passed: Sistema maneja correctamente valores extremadamente bajos/malos")
    print(f"  Puntaje: {resultado['puntaje_total']}")
    print(f"  Reglas de alto riesgo activadas: {len(reglas_riesgo)}")


def test_sin_certificaciones():
    """
    Test 4: Verificar comportamiento cuando no hay certificaciones (lista vacía)
    """
    datos_sin_cert = {
        'liquidez_corriente': 1.5,
        'endeudamiento': 40,
        'rentabilidad': 10,
        'anos_operacion': 5,
        'cumplimiento_entregas': 90,
        'capacidad_produccion': 10000,
        'demanda_estimada': 8000,
        'certificaciones_calidad': [],  # Lista vacía
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 4.0,
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_sin_cert)
    
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    # Debe activarse la regla de sin certificaciones
    assert 'sin_certificaciones' in reglas_activadas, \
        "Debe activarse la regla de sin certificaciones cuando la lista está vacía"
    
    # NO debe activarse la regla de múltiples certificaciones
    assert 'certificaciones_multiples' not in reglas_activadas, \
        "No debe activarse la regla de múltiples certificaciones con lista vacía"
    
    print("✓ Test passed: Sistema maneja correctamente ausencia de certificaciones")


def test_capacidad_igual_demanda():
    """
    Test 5: Verificar comportamiento cuando capacidad = demanda (sin holgura)
    """
    datos_capacidad_justa = {
        'liquidez_corriente': 1.8,
        'endeudamiento': 35,
        'rentabilidad': 12,
        'anos_operacion': 8,
        'cumplimiento_entregas': 93,
        'capacidad_produccion': 10000,
        'demanda_estimada': 10000,  # Exactamente igual
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
    
    resultado = evaluar_proveedor(datos_capacidad_justa)
    
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    # NO debe activarse capacidad insuficiente (capacidad >= demanda)
    assert 'capacidad_insuficiente' not in reglas_activadas, \
        "No debe activarse capacidad insuficiente cuando capacidad = demanda"
    
    # NO debe activarse capacidad sobrada (no es >= 1.5x demanda)
    assert 'capacidad_sobrada' not in reglas_activadas, \
        "No debe activarse capacidad sobrada cuando capacidad = demanda"
    
    print("✓ Test passed: Sistema maneja correctamente capacidad igual a demanda")


def test_cero_demandas_legales():
    """
    Test 6: Verificar que cero demandas legales active la regla correcta
    """
    datos_sin_demandas = {
        'liquidez_corriente': 1.5,
        'endeudamiento': 40,
        'rentabilidad': 10,
        'anos_operacion': 7,
        'cumplimiento_entregas': 90,
        'capacidad_produccion': 12000,
        'demanda_estimada': 10000,
        'certificaciones_calidad': ['ISO 9001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,  # Cero demandas
        'calificacion_mercado': 4.0,
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_sin_demandas)
    
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    assert 'sin_demandas' in reglas_activadas, \
        "Debe activarse la regla 'sin_demandas' cuando demandas_legales = 0"
    
    assert 'multiples_demandas' not in reglas_activadas, \
        "No debe activarse 'multiples_demandas' con 0 demandas"
    
    print("✓ Test passed: Sistema maneja correctamente cero demandas legales")


def test_todos_cumplimientos_legales():
    """
    Test 7: Verificar que se active la regla de cumplimiento legal total
    """
    datos_legal_perfecto = {
        'liquidez_corriente': 1.5,
        'endeudamiento': 40,
        'rentabilidad': 10,
        'anos_operacion': 7,
        'cumplimiento_entregas': 90,
        'capacidad_produccion': 12000,
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
    
    resultado = evaluar_proveedor(datos_legal_perfecto)
    
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    assert 'cumplimiento_legal_total' in reglas_activadas, \
        "Debe activarse 'cumplimiento_legal_total' cuando todos los aspectos legales son positivos"
    
    print("✓ Test passed: Se activa correctamente la regla de cumplimiento legal total")


def test_esg_completo():
    """
    Test 8: Verificar que se active la regla ESG cuando prácticas éticas y ambientales son positivas
    """
    datos_esg = {
        'liquidez_corriente': 1.5,
        'endeudamiento': 40,
        'rentabilidad': 10,
        'anos_operacion': 7,
        'cumplimiento_entregas': 90,
        'capacidad_produccion': 12000,
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
    
    resultado = evaluar_proveedor(datos_esg)
    
    reglas_activadas = [r['regla'] for r in resultado['reglas_activadas']]
    
    assert 'esg_positivo' in reglas_activadas, \
        "Debe activarse 'esg_positivo' cuando hay prácticas éticas y responsabilidad ambiental"
    
    print("✓ Test passed: Se activa correctamente la regla ESG positivo")


if __name__ == "__main__":
    print("=" * 80)
    print("EJECUTANDO TESTS DE CASOS BORDE")
    print("=" * 80)
    print()
    
    test_valores_exactos_en_umbrales()
    print()
    test_valores_extremos_altos()
    print()
    test_valores_extremos_bajos()
    print()
    test_sin_certificaciones()
    print()
    test_capacidad_igual_demanda()
    print()
    test_cero_demandas_legales()
    print()
    test_todos_cumplimientos_legales()
    print()
    test_esg_completo()
    print()
    
    print("=" * 80)
    print("✓ TODOS LOS TESTS DE CASOS BORDE PASARON EXITOSAMENTE")
    print("=" * 80)