"""
Tests de explicación
Valida que el sistema pueda explicar sus decisiones de forma clara y trazable
"""

import pytest
from engine import evaluar_proveedor, Explicador, GeneradorReporte


def test_explicacion_contiene_trazabilidad():
    """
    Test 1: Verificar que la explicación contenga trazabilidad completa de reglas
    """
    datos_proveedor = {
        'liquidez_corriente': 1.8,
        'endeudamiento': 45,
        'rentabilidad': 12,
        'anos_operacion': 8,
        'cumplimiento_entregas': 92,
        'capacidad_produccion': 15000,
        'demanda_estimada': 10000,
        'certificaciones_calidad': ['ISO 9001', 'ISO 14001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 4.2,
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_proveedor)
    explicacion = Explicador.generar_explicacion_detallada(resultado)
    
    # Verificar estructura de la explicación
    assert 'trazabilidad' in explicacion, "La explicación debe contener trazabilidad"
    assert 'resumen_ejecutivo' in explicacion, "La explicación debe contener resumen ejecutivo"
    assert 'analisis_por_dimension' in explicacion, "La explicación debe contener análisis por dimensión"
    assert 'factores_criticos' in explicacion, "La explicación debe contener factores críticos"
    assert 'recomendaciones' in explicacion, "La explicación debe contener recomendaciones"
    
    # Verificar trazabilidad
    trazabilidad = explicacion['trazabilidad']
    assert len(trazabilidad) > 0, "Debe haber al menos una regla en la trazabilidad"
    
    # Cada regla debe tener la estructura esperada
    for regla in trazabilidad:
        assert 'regla' in regla, "Cada regla debe tener nombre"
        assert 'categoria' in regla, "Cada regla debe tener categoría"
        assert 'impacto' in regla, "Cada regla debe explicar su impacto"
        assert 'tipo' in regla, "Cada regla debe indicar si aumenta o reduce riesgo"
        assert 'justificacion' in regla, "Cada regla debe tener justificación"
    
    print("✓ Test passed: La explicación contiene trazabilidad completa")
    print(f"  Total de reglas explicadas: {len(trazabilidad)}")


def test_explicacion_justifica_decision():
    """
    Test 2: Verificar que el sistema pueda explicar POR QUÉ tomó una decisión específica
    """
    # Caso: Proveedor con alto riesgo financiero
    datos_riesgo_financiero = {
        'liquidez_corriente': 0.7,
        'endeudamiento': 80,
        'rentabilidad': -3,
        'anos_operacion': 10,
        'cumplimiento_entregas': 95,
        'capacidad_produccion': 20000,
        'demanda_estimada': 15000,
        'certificaciones_calidad': ['ISO 9001', 'ISO 14001'],
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 4.5,
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_riesgo_financiero)
    explicacion = Explicador.generar_explicacion_detallada(resultado)
    
    # El sistema debe identificar que el problema es financiero
    dimensiones = explicacion['analisis_por_dimension']
    
    assert 'financiero' in dimensiones, "Debe analizar la dimensión financiera"
    
    dim_financiera = dimensiones['financiero']
    assert dim_financiera['puntaje'] > 0, "La dimensión financiera debe tener puntaje de riesgo positivo"
    
    # Verificar que hay factores críticos identificados
    factores = explicacion['factores_criticos']
    assert len(factores) > 0, "Debe identificar factores críticos"
    
    # Debe haber factores de riesgo mencionados
    tiene_riesgos = any('RIESGO' in f['tipo'] for f in factores)
    assert tiene_riesgos, "Debe identificar los principales riesgos"
    
    # Verificar que las justificaciones mencionan los problemas financieros
    reglas_financieras = [r for r in resultado['reglas_activadas'] 
                          if r['categoria'] == 'financiero']
    
    assert len(reglas_financieras) > 0, "Deben activarse reglas financieras"
    
    # Las justificaciones deben mencionar liquidez, endeudamiento o rentabilidad
    justificaciones = [r['justificacion'].lower() for r in reglas_financieras]
    temas_mencionados = any(
        'liquidez' in j or 'endeudamiento' in j or 'rentabilidad' in j 
        for j in justificaciones
    )
    
    assert temas_mencionados, "Las justificaciones deben explicar los problemas financieros específicos"
    
    print("✓ Test passed: El sistema justifica correctamente sus decisiones")
    print(f"  Problema identificado: Riesgo financiero (puntaje: {dim_financiera['puntaje']})")
    print(f"  Reglas financieras activadas: {len(reglas_financieras)}")


def test_explicacion_identifica_fortalezas_y_debilidades():
    """
    Test 3: Verificar que el sistema identifique tanto fortalezas como debilidades
    """
    # Proveedor con perfil mixto
    datos_mixto = {
        'liquidez_corriente': 2.5,  # Excelente
        'endeudamiento': 25,  # Muy bueno
        'rentabilidad': 18,  # Excelente
        'anos_operacion': 2,  # Débil
        'cumplimiento_entregas': 75,  # Débil
        'capacidad_produccion': 8000,
        'demanda_estimada': 10000,  # Débil (capacidad insuficiente)
        'certificaciones_calidad': [],  # Débil
        'licencias_vigentes': True,
        'certificado_tributario': True,
        'cumplimiento_laboral': True,
        'demandas_legales': 0,
        'calificacion_mercado': 4.5,  # Bueno
        'incidentes_seguridad': 0,
        'practicas_eticas': True,
        'responsabilidad_ambiental': True
    }
    
    resultado = evaluar_proveedor(datos_mixto)
    explicacion = Explicador.generar_explicacion_detallada(resultado)
    
    factores = explicacion['factores_criticos']
    
    # Debe haber tanto riesgos como fortalezas
    tipos_factores = [f['tipo'] for f in factores]
    
    tiene_riesgos = any('RIESGO' in tipo for tipo in tipos_factores)
    tiene_fortalezas = any('FORTALEZAS' in tipo for tipo in tipos_factores)
    
    assert tiene_riesgos, "Debe identificar los riesgos (debilidades operacionales)"
    assert tiene_fortalezas, "Debe identificar las fortalezas (salud financiera)"
    
    # Verificar que hay reglas tanto positivas como negativas
    impactos = [r['impacto'] for r in resultado['reglas_activadas']]
    hay_positivos = any(i > 0 for i in impactos)
    hay_negativos = any(i < 0 for i in impactos)
    
    assert hay_positivos and hay_negativos, \
        "Debe haber reglas que aumentan el riesgo Y reglas que lo reducen"
    
    print("✓ Test passed: El sistema identifica correctamente fortalezas y debilidades")
    print(f"  Fortalezas identificadas: {len([i for i in impactos if i < 0])}")
    print(f"  Debilidades identificadas: {len([i for i in impactos if i > 0])}")


def test_explicacion_por_dimension():
    """
    Test 4: Verificar que el sistema analice cada dimensión por separado
    """
    datos_proveedor = {
        'liquidez_corriente': 1.8,
        'endeudamiento': 40,
        'rentabilidad': 12,
        'anos_operacion': 8,
        'cumplimiento_entregas': 92,
        'capacidad_produccion': 15000,
        'demanda_estimada': 10000,
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
    
    resultado = evaluar_proveedor(datos_proveedor)
    explicacion = Explicador.generar_explicacion_detallada(resultado)
    
    dimensiones = explicacion['analisis_por_dimension']
    
    # Verificar que están todas las dimensiones
    dimensiones_requeridas = ['financiero', 'operacional', 'legal', 'reputacional']
    
    for dim in dimensiones_requeridas:
        assert dim in dimensiones, f"Falta la dimensión {dim}"
        
        datos_dim = dimensiones[dim]
        
        # Cada dimensión debe tener la estructura esperada
        assert 'nombre' in datos_dim, f"Dimensión {dim} debe tener nombre"
        assert 'puntaje' in datos_dim, f"Dimensión {dim} debe tener puntaje"
        assert 'nivel' in datos_dim, f"Dimensión {dim} debe tener nivel de riesgo"
        assert 'descripcion' in datos_dim, f"Dimensión {dim} debe tener descripción"
        assert 'reglas_aplicadas' in datos_dim, f"Dimensión {dim} debe indicar cuántas reglas se aplicaron"
        assert 'contribucion_riesgo' in datos_dim, f"Dimensión {dim} debe indicar su contribución al riesgo total"
    
    print("✓ Test passed: El sistema analiza correctamente cada dimensión")
    print("  Dimensiones analizadas:")
    for dim, datos in dimensiones.items():
        print(f"    - {datos['nombre']}: {datos['nivel']} (puntaje: {datos['puntaje']})")


def test_explicacion_genera_recomendaciones():
    """
    Test 5: Verificar que el sistema genere recomendaciones accionables
    """
    datos_proveedor = {
        'liquidez_corriente': 1.5,
        'endeudamiento': 50,
        'rentabilidad': 10,
        'anos_operacion': 6,
        'cumplimiento_entregas': 88,
        'capacidad_produccion': 12000,
        'demanda_estimada': 10000,
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
    
    resultado = evaluar_proveedor(datos_proveedor)
    explicacion = Explicador.generar_explicacion_detallada(resultado)
    
    recomendaciones = explicacion['recomendaciones']
    
    # Debe haber recomendaciones
    assert len(recomendaciones) > 0, "Debe generar al menos una recomendación"
    
    # Las recomendaciones deben ser strings no vacíos
    for rec in recomendaciones:
        assert isinstance(rec, str), "Cada recomendación debe ser un string"
        assert len(rec) > 10, "Las recomendaciones deben ser sustanciales"
    
    # Debe incluir información sobre quién debe aprobar
    texto_recomendaciones = ' '.join(recomendaciones).lower()
    menciona_aprobador = any(
        palabra in texto_recomendaciones 
        for palabra in ['gerente', 'director', 'comité', 'aprobación']
    )
    
    assert menciona_aprobador, "Las recomendaciones deben indicar quién debe aprobar la decisión"
    
    print("✓ Test passed: El sistema genera recomendaciones accionables")
    print(f"  Total de recomendaciones: {len(recomendaciones)}")


def test_explicacion_en_texto_plano():
    """
    Test 6: Verificar que se pueda generar explicación en texto plano
    """
    datos_proveedor = {
        'liquidez_corriente': 1.8,
        'endeudamiento': 40,
        'rentabilidad': 12,
        'anos_operacion': 8,
        'cumplimiento_entregas': 92,
        'capacidad_produccion': 15000,
        'demanda_estimada': 10000,
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
    
    resultado = evaluar_proveedor(datos_proveedor)
    texto = Explicador.generar_explicacion_texto(resultado)
    
    # Verificar que es un string
    assert isinstance(texto, str), "La explicación en texto debe ser un string"
    
    # Verificar que contiene información clave
    assert 'NIVEL DE RIESGO' in texto, "Debe incluir el nivel de riesgo"
    assert 'PUNTAJE' in texto, "Debe incluir el puntaje"
    assert 'TRAZABILIDAD' in texto, "Debe incluir trazabilidad"
    assert 'DIMENSIÓN' in texto, "Debe incluir análisis por dimensión"
    
    # Debe tener un tamaño razonable
    assert len(texto) > 500, "La explicación debe ser sustancial"
    
    print("✓ Test passed: Se genera correctamente explicación en texto plano")
    print(f"  Longitud del texto: {len(texto)} caracteres")


def test_reporte_json_completo():
    """
    Test 7: Verificar que se pueda generar un reporte JSON completo
    """
    datos_proveedor = {
        'nombre': 'Test Corp',
        'ruc': '12345678901',
        'pais': 'Perú',
        'sector': 'Manufactura',
        'liquidez_corriente': 1.8,
        'endeudamiento': 40,
        'rentabilidad': 12,
        'anos_operacion': 8,
        'cumplimiento_entregas': 92,
        'capacidad_produccion': 15000,
        'demanda_estimada': 10000,
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
    
    # Extraer datos para evaluación (sin metadata del proveedor)
    datos_evaluacion = {k: v for k, v in datos_proveedor.items() 
                       if k not in ['nombre', 'ruc', 'pais', 'sector']}
    
    resultado = evaluar_proveedor(datos_evaluacion)
    reporte = GeneradorReporte.generar_reporte_json(resultado, datos_proveedor)
    
    # Verificar estructura del reporte
    assert 'metadata' in reporte, "El reporte debe contener metadata"
    assert 'proveedor' in reporte, "El reporte debe contener datos del proveedor"
    assert 'evaluacion' in reporte, "El reporte debe contener la evaluación"
    assert 'explicacion' in reporte, "El reporte debe contener la explicación"
    assert 'disclaimer' in reporte, "El reporte debe contener el disclaimer"
    
    # Verificar metadata
    assert 'fecha_evaluacion' in reporte['metadata']
    assert 'version_sistema' in reporte['metadata']
    
    # Verificar que se puede serializar a JSON
    import json
    try:
        json_str = json.dumps(reporte, indent=2, ensure_ascii=False)
        assert len(json_str) > 1000, "El reporte JSON debe ser sustancial"
    except Exception as e:
        pytest.fail(f"No se pudo serializar el reporte a JSON: {e}")
    
    print("✓ Test passed: Se genera correctamente reporte JSON completo")
    print(f"  Tamaño del reporte: {len(json_str)} caracteres")


if __name__ == "__main__":
    print("=" * 80)
    print("EJECUTANDO TESTS DE EXPLICACIÓN")
    print("=" * 80)
    print()
    
    test_explicacion_contiene_trazabilidad()
    print()
    test_explicacion_justifica_decision()
    print()
    test_explicacion_identifica_fortalezas_y_debilidades()
    print()
    test_explicacion_por_dimension()
    print()
    test_explicacion_genera_recomendaciones()
    print()
    test_explicacion_en_texto_plano()
    print()
    test_reporte_json_completo()
    print()
    
    print("=" * 80)
    print("✓ TODOS LOS TESTS DE EXPLICACIÓN PASARON EXITOSAMENTE")
    print("=" * 80)