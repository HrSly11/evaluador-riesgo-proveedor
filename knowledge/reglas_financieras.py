"""
Reglas Financieras - Base de Conocimiento
Define las reglas para evaluar la salud financiera de proveedores
"""

# Umbrales financieros basados en estándares de la industria
UMBRALES_FINANCIEROS = {
    'liquidez': {
        'excelente': 2.0,      # Ratio >= 2.0
        'aceptable': 1.0,      # Ratio >= 1.0
        'riesgoso': 1.0        # Ratio < 1.0
    },
    'endeudamiento': {
        'bajo': 40,            # Endeudamiento < 40%
        'moderado': 70,        # Endeudamiento entre 40-70%
        'alto': 70             # Endeudamiento > 70%
    },
    'rentabilidad': {
        'excelente': 15,       # Rentabilidad >= 15%
        'aceptable': 5,        # Rentabilidad >= 5%
        'negativa': 0          # Rentabilidad < 0%
    }
}

# Definición de reglas financieras con su lógica y pesos
REGLAS_FINANCIERAS = {
    'liquidez_excelente': {
        'descripcion': 'El proveedor tiene excelente capacidad de pago a corto plazo',
        'condicion': lambda datos: datos.get('liquidez_corriente', 0) >= UMBRALES_FINANCIEROS['liquidez']['excelente'],
        'impacto': -15,
        'categoria': 'financiero',
        'severidad': 'positivo',
        'justificacion': 'Ratio de liquidez corriente >= 2.0 indica sólida capacidad para cubrir obligaciones inmediatas'
    },
    
    'liquidez_aceptable': {
        'descripcion': 'El proveedor tiene capacidad de pago moderada',
        'condicion': lambda datos: UMBRALES_FINANCIEROS['liquidez']['aceptable'] <= datos.get('liquidez_corriente', 0) < UMBRALES_FINANCIEROS['liquidez']['excelente'],
        'impacto': -5,
        'categoria': 'financiero',
        'severidad': 'bajo',
        'justificacion': 'Ratio de liquidez entre 1.0 y 2.0 es aceptable para operaciones normales'
    },
    
    'liquidez_riesgosa': {
        'descripcion': 'El proveedor tiene baja capacidad de pago a corto plazo',
        'condicion': lambda datos: datos.get('liquidez_corriente', 0) < UMBRALES_FINANCIEROS['liquidez']['riesgoso'],
        'impacto': 25,
        'categoria': 'financiero',
        'severidad': 'alto',
        'justificacion': 'Ratio de liquidez < 1.0 indica dificultades para cumplir obligaciones de corto plazo'
    },
    
    'endeudamiento_bajo': {
        'descripcion': 'Nivel de endeudamiento saludable',
        'condicion': lambda datos: datos.get('endeudamiento', 100) < UMBRALES_FINANCIEROS['endeudamiento']['bajo'],
        'impacto': -10,
        'categoria': 'financiero',
        'severidad': 'positivo',
        'justificacion': 'Endeudamiento < 40% demuestra estructura de capital conservadora y bajo riesgo financiero'
    },
    
    'endeudamiento_moderado': {
        'descripcion': 'Nivel de endeudamiento moderado',
        'condicion': lambda datos: UMBRALES_FINANCIEROS['endeudamiento']['bajo'] <= datos.get('endeudamiento', 100) <= UMBRALES_FINANCIEROS['endeudamiento']['moderado'],
        'impacto': 5,
        'categoria': 'financiero',
        'severidad': 'bajo',
        'justificacion': 'Endeudamiento entre 40-70% es manejable pero requiere monitoreo'
    },
    
    'endeudamiento_alto': {
        'descripcion': 'Nivel de endeudamiento peligroso',
        'condicion': lambda datos: datos.get('endeudamiento', 0) > UMBRALES_FINANCIEROS['endeudamiento']['alto'],
        'impacto': 20,
        'categoria': 'financiero',
        'severidad': 'alto',
        'justificacion': 'Endeudamiento > 70% representa alto riesgo de insolvencia y dificultades financieras'
    },
    
    'rentabilidad_excelente': {
        'descripcion': 'Rentabilidad sobresaliente',
        'condicion': lambda datos: datos.get('rentabilidad', -100) >= UMBRALES_FINANCIEROS['rentabilidad']['excelente'],
        'impacto': -12,
        'categoria': 'financiero',
        'severidad': 'positivo',
        'justificacion': 'Rentabilidad >= 15% indica negocio muy rentable y sostenible en el tiempo'
    },
    
    'rentabilidad_aceptable': {
        'descripcion': 'Rentabilidad aceptable',
        'condicion': lambda datos: UMBRALES_FINANCIEROS['rentabilidad']['aceptable'] <= datos.get('rentabilidad', -100) < UMBRALES_FINANCIEROS['rentabilidad']['excelente'],
        'impacto': -5,
        'categoria': 'financiero',
        'severidad': 'bajo',
        'justificacion': 'Rentabilidad entre 5-15% es adecuada para operaciones comerciales estables'
    },
    
    'rentabilidad_negativa': {
        'descripcion': 'Rentabilidad negativa - operando con pérdidas',
        'condicion': lambda datos: datos.get('rentabilidad', 0) < UMBRALES_FINANCIEROS['rentabilidad']['negativa'],
        'impacto': 18,
        'categoria': 'financiero',
        'severidad': 'alto',
        'justificacion': 'Rentabilidad negativa indica que el proveedor está operando con pérdidas, comprometiendo su viabilidad'
    },
    
    'crisis_financiera': {
        'descripcion': 'Crisis financiera inminente',
        'condicion': lambda datos: (
            datos.get('liquidez_corriente', 10) < UMBRALES_FINANCIEROS['liquidez']['riesgoso'] and
            datos.get('endeudamiento', 0) > UMBRALES_FINANCIEROS['endeudamiento']['alto']
        ),
        'impacto': 30,
        'categoria': 'financiero',
        'severidad': 'critico',
        'justificacion': 'Combinación de baja liquidez y alto endeudamiento indica riesgo de quiebra inminente'
    },
    
    'salud_financiera_robusta': {
        'descripcion': 'Salud financiera excepcional',
        'condicion': lambda datos: (
            datos.get('liquidez_corriente', 0) >= UMBRALES_FINANCIEROS['liquidez']['excelente'] and
            datos.get('endeudamiento', 100) < UMBRALES_FINANCIEROS['endeudamiento']['bajo'] and
            datos.get('rentabilidad', -100) >= UMBRALES_FINANCIEROS['rentabilidad']['excelente']
        ),
        'impacto': -20,
        'categoria': 'financiero',
        'severidad': 'positivo',
        'justificacion': 'Combinación de excelente liquidez, bajo endeudamiento y alta rentabilidad demuestra solidez financiera excepcional'
    }
}

# Documentación de indicadores financieros
DOCUMENTACION_INDICADORES = {
    'liquidez_corriente': {
        'nombre': 'Ratio de Liquidez Corriente',
        'formula': 'Activo Corriente / Pasivo Corriente',
        'interpretacion': 'Mide la capacidad de la empresa para pagar sus deudas de corto plazo con sus activos líquidos',
        'ideal': '>= 2.0',
        'aceptable': '1.0 - 2.0',
        'riesgoso': '< 1.0'
    },
    'endeudamiento': {
        'nombre': 'Ratio de Endeudamiento',
        'formula': '(Pasivo Total / Activo Total) × 100',
        'interpretacion': 'Indica qué porcentaje de los activos está financiado con deuda',
        'ideal': '< 40%',
        'aceptable': '40% - 70%',
        'riesgoso': '> 70%'
    },
    'rentabilidad': {
        'nombre': 'Margen de Rentabilidad Neta',
        'formula': '(Utilidad Neta / Ventas Totales) × 100',
        'interpretacion': 'Indica qué porcentaje de las ventas se convierte en utilidad',
        'ideal': '>= 15%',
        'aceptable': '5% - 15%',
        'riesgoso': '< 0%'
    }
}

# Factores de ajuste por industria (opcional)
AJUSTES_POR_INDUSTRIA = {
    'tecnologia': {
        'liquidez': {'multiplicador': 0.9},  # Menor liquidez es aceptable
        'endeudamiento': {'multiplicador': 1.1},  # Mayor endeudamiento es aceptable
        'rentabilidad': {'multiplicador': 1.2}  # Se espera mayor rentabilidad
    },
    'manufactura': {
        'liquidez': {'multiplicador': 1.0},
        'endeudamiento': {'multiplicador': 1.0},
        'rentabilidad': {'multiplicador': 1.0}
    },
    'servicios': {
        'liquidez': {'multiplicador': 1.1},
        'endeudamiento': {'multiplicador': 0.9},
        'rentabilidad': {'multiplicador': 1.1}
    },
    'construccion': {
        'liquidez': {'multiplicador': 0.8},  # Menor liquidez por ciclo de proyectos
        'endeudamiento': {'multiplicador': 1.2},  # Mayor endeudamiento es común
        'rentabilidad': {'multiplicador': 0.9}
    }
}