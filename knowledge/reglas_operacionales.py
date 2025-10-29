"""
Reglas Operacionales - Base de Conocimiento
Define las reglas para evaluar la capacidad operativa de proveedores
"""

# Umbrales operacionales
UMBRALES_OPERACIONALES = {
    'experiencia': {
        'consolidado': 10,     # >= 10 años
        'establecido': 5,      # >= 5 años
        'nuevo': 2             # < 2 años
    },
    'cumplimiento': {
        'excelente': 95,       # >= 95%
        'aceptable': 85,       # >= 85%
        'deficiente': 80       # < 80%
    },
    'capacidad': {
        'holgada': 1.5,        # 150% de la demanda
        'justa': 1.0,          # 100% de la demanda
        'insuficiente': 1.0    # < 100% de la demanda
    }
}

# Certificaciones reconocidas internacionalmente
CERTIFICACIONES_RECONOCIDAS = [
    'ISO 9001',      # Gestión de Calidad
    'ISO 14001',     # Gestión Ambiental
    'OHSAS 18001',   # Seguridad y Salud Ocupacional
    'ISO 45001',     # Sistema de Gestión de SST
    'HACCP',         # Análisis de Peligros y Puntos Críticos de Control
    'BRC',           # British Retail Consortium
    'IFS',           # International Featured Standards
    'ISO 27001',     # Seguridad de la Información
    'SA 8000',       # Responsabilidad Social
    'FSC',           # Forest Stewardship Council
    'BASC'           # Business Alliance for Secure Commerce
]

REGLAS_OPERACIONALES = {
    'experiencia_consolidada': {
        'descripcion': 'Proveedor con amplia trayectoria en el mercado',
        'condicion': lambda datos: datos.get('anos_operacion', 0) >= UMBRALES_OPERACIONALES['experiencia']['consolidado'],
        'impacto': -10,
        'categoria': 'operacional',
        'severidad': 'positivo',
        'justificacion': 'Más de 10 años en el mercado demuestran estabilidad, experiencia y capacidad de adaptación'
    },
    
    'experiencia_establecida': {
        'descripcion': 'Proveedor con experiencia moderada',
        'condicion': lambda datos: UMBRALES_OPERACIONALES['experiencia']['nuevo'] <= datos.get('anos_operacion', 0) < UMBRALES_OPERACIONALES['experiencia']['consolidado'],
        'impacto': -3,
        'categoria': 'operacional',
        'severidad': 'bajo',
        'justificacion': 'Entre 2 y 10 años de operación indica experiencia en desarrollo con historial verificable'
    },
    
    'proveedor_nuevo': {
        'descripcion': 'Proveedor con poca experiencia',
        'condicion': lambda datos: datos.get('anos_operacion', 0) < UMBRALES_OPERACIONALES['experiencia']['nuevo'],
        'impacto': 15,
        'categoria': 'operacional',
        'severidad': 'alto',
        'justificacion': 'Menos de 2 años de operación representa falta de trayectoria y mayor riesgo de discontinuidad'
    },
    
    'cumplimiento_excelente': {
        'descripcion': 'Excelente historial de entregas',
        'condicion': lambda datos: datos.get('cumplimiento_entregas', 0) >= UMBRALES_OPERACIONALES['cumplimiento']['excelente'],
        'impacto': -15,
        'categoria': 'operacional',
        'severidad': 'positivo',
        'justificacion': 'Cumplimiento >= 95% demuestra alta confiabilidad y compromiso con plazos'
    },
    
    'cumplimiento_aceptable': {
        'descripcion': 'Historial de entregas aceptable',
        'condicion': lambda datos: UMBRALES_OPERACIONALES['cumplimiento']['aceptable'] <= datos.get('cumplimiento_entregas', 0) < UMBRALES_OPERACIONALES['cumplimiento']['excelente'],
        'impacto': -5,
        'categoria': 'operacional',
        'severidad': 'bajo',
        'justificacion': 'Cumplimiento entre 85-95% es aceptable con margen de mejora'
    },
    
    'cumplimiento_deficiente': {
        'descripcion': 'Historial de entregas deficiente',
        'condicion': lambda datos: datos.get('cumplimiento_entregas', 100) < UMBRALES_OPERACIONALES['cumplimiento']['deficiente'],
        'impacto': 20,
        'categoria': 'operacional',
        'severidad': 'alto',
        'justificacion': 'Cumplimiento < 80% indica problemas recurrentes y alta probabilidad de incumplimientos futuros'
    },
    
    'capacidad_sobrada': {
        'descripcion': 'Capacidad de producción holgada',
        'condicion': lambda datos: (
            datos.get('capacidad_produccion', 0) >= 
            datos.get('demanda_estimada', 1) * UMBRALES_OPERACIONALES['capacidad']['holgada']
        ),
        'impacto': -8,
        'categoria': 'operacional',
        'severidad': 'positivo',
        'justificacion': 'Capacidad 50% superior a la demanda permite responder a picos y emergencias'
    },
    
    'capacidad_justa': {
        'descripcion': 'Capacidad ajustada a la demanda',
        'condicion': lambda datos: (
            datos.get('demanda_estimada', 0) <= datos.get('capacidad_produccion', 0) < 
            datos.get('demanda_estimada', 0) * UMBRALES_OPERACIONALES['capacidad']['holgada']
        ),
        'impacto': 0,
        'categoria': 'operacional',
        'severidad': 'neutro',
        'justificacion': 'Capacidad igual a la demanda sin margen para incrementos'
    },
    
    'capacidad_insuficiente': {
        'descripcion': 'Capacidad de producción insuficiente',
        'condicion': lambda datos: (
            datos.get('capacidad_produccion', 0) < 
            datos.get('demanda_estimada', float('inf'))
        ),
        'impacto': 22,
        'categoria': 'operacional',
        'severidad': 'alto',
        'justificacion': 'Capacidad menor a la demanda genera alto riesgo de desabastecimiento y entregas parciales'
    },
    
    'certificaciones_multiples': {
        'descripcion': 'Múltiples certificaciones de calidad',
        'condicion': lambda datos: (
            isinstance(datos.get('certificaciones_calidad', []), list) and 
            len(datos.get('certificaciones_calidad', [])) >= 2
        ),
        'impacto': -12,
        'categoria': 'operacional',
        'severidad': 'positivo',
        'justificacion': 'Múltiples certificaciones demuestran procesos estandarizados, auditados y compromiso con la calidad'
    },
    
    'certificacion_unica': {
        'descripcion': 'Una certificación de calidad',
        'condicion': lambda datos: (
            isinstance(datos.get('certificaciones_calidad', []), list) and 
            len(datos.get('certificaciones_calidad', [])) == 1
        ),
        'impacto': -5,
        'categoria': 'operacional',
        'severidad': 'bajo',
        'justificacion': 'Cuenta con certificación básica de calidad que valida sus procesos'
    },
    
    'sin_certificaciones': {
        'descripcion': 'Sin certificaciones de calidad',
        'condicion': lambda datos: (
            not datos.get('certificaciones_calidad') or 
            len(datos.get('certificaciones_calidad', [])) == 0
        ),
        'impacto': 10,
        'categoria': 'operacional',
        'severidad': 'moderado',
        'justificacion': 'Falta de certificaciones representa ausencia de validación externa de procesos y calidad'
    },
    
    'proveedor_maduro_confiable': {
        'descripcion': 'Proveedor maduro y altamente confiable',
        'condicion': lambda datos: (
            datos.get('anos_operacion', 0) >= UMBRALES_OPERACIONALES['experiencia']['consolidado'] and
            datos.get('cumplimiento_entregas', 0) >= UMBRALES_OPERACIONALES['cumplimiento']['excelente'] and
            len(datos.get('certificaciones_calidad', [])) >= 2
        ),
        'impacto': -15,
        'categoria': 'operacional',
        'severidad': 'positivo',
        'justificacion': 'Combinación de experiencia, cumplimiento excelente y certificaciones múltiples indica proveedor de clase mundial'
    },
    
    'riesgo_operacional_critico': {
        'descripcion': 'Riesgo operacional crítico',
        'condicion': lambda datos: (
            datos.get('anos_operacion', 0) < UMBRALES_OPERACIONALES['experiencia']['nuevo'] and
            datos.get('cumplimiento_entregas', 100) < UMBRALES_OPERACIONALES['cumplimiento']['deficiente'] and
            datos.get('capacidad_produccion', 0) < datos.get('demanda_estimada', 0)
        ),
        'impacto': 25,
        'categoria': 'operacional',
        'severidad': 'critico',
        'justificacion': 'Combinación de inexperiencia, bajo cumplimiento y capacidad insuficiente representa riesgo operacional inaceptable'
    }
}

# Documentación de indicadores operacionales
DOCUMENTACION_INDICADORES_OPERACIONALES = {
    'anos_operacion': {
        'nombre': 'Años de Operación',
        'descripcion': 'Tiempo que el proveedor ha estado operando en el mercado',
        'importancia': 'Indica estabilidad, experiencia y capacidad de supervivencia',
        'rango_ideal': '>= 10 años'
    },
    'cumplimiento_entregas': {
        'nombre': 'Tasa de Cumplimiento de Entregas',
        'formula': '(Entregas a tiempo / Total entregas) × 100',
        'descripcion': 'Porcentaje de entregas realizadas en el plazo acordado',
        'rango_ideal': '>= 95%'
    },
    'capacidad_produccion': {
        'nombre': 'Capacidad de Producción',
        'descripcion': 'Volumen máximo que el proveedor puede producir en un periodo',
        'importancia': 'Determina si puede satisfacer la demanda actual y futura',
        'recomendacion': 'Debe ser al menos 20% mayor que la demanda estimada'
    },
    'certificaciones_calidad': {
        'nombre': 'Certificaciones de Calidad',
        'descripcion': 'Certificaciones internacionales que validan procesos y estándares',
        'ejemplos': CERTIFICACIONES_RECONOCIDAS,
        'importancia': 'Garantiza que el proveedor cumple estándares internacionales auditados'
    }
}

# Mejores prácticas operacionales
MEJORES_PRACTICAS = {
    'gestion_inventario': [
        'Sistema de inventario en tiempo real',
        'Just-in-time para reducir costos',
        'Stock de seguridad adecuado',
        'Trazabilidad completa de lotes'
    ],
    'gestion_calidad': [
        'Inspección de calidad en múltiples puntos',
        'Auditorías internas periódicas',
        'Planes de acción correctiva documentados',
        'Mejora continua implementada'
    ],
    'gestion_entregas': [
        'Sistema de tracking en línea',
        'Comunicación proactiva de retrasos',
        'Planes de contingencia documentados',
        'SLA (Service Level Agreement) claros'
    ]
}