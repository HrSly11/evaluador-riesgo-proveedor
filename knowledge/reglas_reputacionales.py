"""
Reglas Reputacionales - Base de Conocimiento
Define las reglas para evaluar la reputación y confianza de proveedores
"""

# Umbrales reputacionales
UMBRALES_REPUTACIONALES = {
    'calificacion': {
        'excelente': 4.5,      # >= 4.5/5.0
        'buena': 3.5,          # >= 3.5/5.0
        'regular': 2.5,        # >= 2.5/5.0
        'deficiente': 2.5      # < 2.5/5.0
    },
    'incidentes': {
        'sin_incidentes': 0,
        'incidentes_menores': 1,
        'incidentes_graves': 2
    },
    'reclamos': {
        'bajo': 2,             # <= 2%
        'moderado': 5,         # <= 5%
        'alto': 5              # > 5%
    }
}

# Factores ESG (Environmental, Social, Governance)
CRITERIOS_ESG = {
    'ambiental': [
        'Gestión de residuos',
        'Eficiencia energética',
        'Huella de carbono',
        'Uso responsable de recursos naturales',
        'Certificaciones ambientales (ISO 14001, etc.)'
    ],
    'social': [
        'Derechos humanos',
        'Condiciones laborales',
        'Diversidad e inclusión',
        'Desarrollo de comunidades',
        'Salud y seguridad ocupacional'
    ],
    'gobernanza': [
        'Transparencia corporativa',
        'Código de ética',
        'Anti-corrupción',
        'Gestión de riesgos',
        'Cumplimiento normativo'
    ]
}

REGLAS_REPUTACIONALES = {
    'reputacion_excelente': {
        'descripcion': 'Excelente reputación en el mercado',
        'condicion': lambda datos: datos.get('calificacion_mercado', 0) >= UMBRALES_REPUTACIONALES['calificacion']['excelente'],
        'impacto': -12,
        'categoria': 'reputacional',
        'severidad': 'positivo',
        'justificacion': 'Calificación >= 4.5/5.0 indica alta satisfacción de clientes y confianza del mercado'
    },
    
    'reputacion_buena': {
        'descripcion': 'Buena reputación en el mercado',
        'condicion': lambda datos: (
            UMBRALES_REPUTACIONALES['calificacion']['buena'] <= 
            datos.get('calificacion_mercado', 0) < 
            UMBRALES_REPUTACIONALES['calificacion']['excelente']
        ),
        'impacto': -5,
        'categoria': 'reputacional',
        'severidad': 'bajo',
        'justificacion': 'Calificación entre 3.5-4.5/5.0 refleja desempeño aceptable con margen de mejora'
    },
    
    'reputacion_regular': {
        'descripcion': 'Reputación regular',
        'condicion': lambda datos: (
            UMBRALES_REPUTACIONALES['calificacion']['regular'] <= 
            datos.get('calificacion_mercado', 0) < 
            UMBRALES_REPUTACIONALES['calificacion']['buena']
        ),
        'impacto': 8,
        'categoria': 'reputacional',
        'severidad': 'moderado',
        'justificacion': 'Calificación entre 2.5-3.5/5.0 sugiere insatisfacción moderada de clientes'
    },
    
    'reputacion_deficiente': {
        'descripcion': 'Reputación deficiente',
        'condicion': lambda datos: datos.get('calificacion_mercado', 5.0) < UMBRALES_REPUTACIONALES['calificacion']['deficiente'],
        'impacto': 18,
        'categoria': 'reputacional',
        'severidad': 'alto',
        'justificacion': 'Calificación < 2.5/5.0 indica percepción muy negativa y alta insatisfacción en el mercado'
    },
    
    'sin_incidentes_seguridad': {
        'descripcion': 'Sin incidentes de seguridad',
        'condicion': lambda datos: datos.get('incidentes_seguridad', 1) == UMBRALES_REPUTACIONALES['incidentes']['sin_incidentes'],
        'impacto': -8,
        'categoria': 'reputacional',
        'severidad': 'positivo',
        'justificacion': 'Ausencia de incidentes de seguridad demuestra operación confiable y gestión de riesgos efectiva'
    },
    
    'incidentes_seguridad_menores': {
        'descripcion': 'Incidentes de seguridad aislados',
        'condicion': lambda datos: datos.get('incidentes_seguridad', 0) == UMBRALES_REPUTACIONALES['incidentes']['incidentes_menores'],
        'impacto': 10,
        'categoria': 'reputacional',
        'severidad': 'moderado',
        'justificacion': 'Un incidente requiere evaluación de causa raíz y acciones correctivas implementadas'
    },
    
    'incidentes_seguridad_graves': {
        'descripcion': 'Múltiples incidentes de seguridad',
        'condicion': lambda datos: datos.get('incidentes_seguridad', 0) >= UMBRALES_REPUTACIONALES['incidentes']['incidentes_graves'],
        'impacto': 25,
        'categoria': 'reputacional',
        'severidad': 'critico',
        'justificacion': 'Múltiples incidentes indican fallas sistemáticas en seguridad y alto riesgo para la cadena de suministro'
    },
    
    'practicas_eticas_verificadas': {
        'descripcion': 'Prácticas éticas verificadas',
        'condicion': lambda datos: datos.get('practicas_eticas', False) == True,
        'impacto': -6,
        'categoria': 'reputacional',
        'severidad': 'positivo',
        'justificacion': 'Prácticas éticas verificadas reducen riesgo reputacional y alinean con estándares corporativos'
    },
    
    'etica_cuestionable': {
        'descripcion': 'Prácticas éticas cuestionables',
        'condicion': lambda datos: datos.get('practicas_eticas', True) == False,
        'impacto': 22,
        'categoria': 'reputacional',
        'severidad': 'alto',
        'justificacion': 'Prácticas éticas cuestionables generan riesgo de escándalos, sanciones y daño reputacional por asociación'
    },
    
    'responsabilidad_ambiental': {
        'descripcion': 'Responsabilidad ambiental verificada',
        'condicion': lambda datos: datos.get('responsabilidad_ambiental', False) == True,
        'impacto': -5,
        'categoria': 'reputacional',
        'severidad': 'positivo',
        'justificacion': 'Compromiso ambiental demuestra visión de largo plazo y cumplimiento de estándares ESG'
    },
    
    'sin_responsabilidad_ambiental': {
        'descripcion': 'Sin prácticas ambientales',
        'condicion': lambda datos: datos.get('responsabilidad_ambiental', True) == False,
        'impacto': 8,
        'categoria': 'reputacional',
        'severidad': 'moderado',
        'justificacion': 'Falta de compromiso ambiental genera riesgo regulatorio y reputacional creciente'
    },
    
    'esg_positivo': {
        'descripcion': 'Perfil ESG positivo',
        'condicion': lambda datos: (
            datos.get('practicas_eticas', False) == True and
            datos.get('responsabilidad_ambiental', False) == True
        ),
        'impacto': -10,
        'categoria': 'reputacional',
        'severidad': 'positivo',
        'justificacion': 'Cumplimiento de criterios ESG (Environmental, Social, Governance) demuestra gestión sostenible y responsable'
    },
    
    'crisis_reputacional': {
        'descripcion': 'Crisis reputacional',
        'condicion': lambda datos: (
            datos.get('calificacion_mercado', 5.0) < UMBRALES_REPUTACIONALES['calificacion']['deficiente'] and
            datos.get('incidentes_seguridad', 0) >= UMBRALES_REPUTACIONALES['incidentes']['incidentes_graves'] and
            datos.get('practicas_eticas', True) == False
        ),
        'impacto': 35,
        'categoria': 'reputacional',
        'severidad': 'critico',
        'justificacion': 'Combinación de mala reputación, incidentes múltiples y ética cuestionable representa riesgo reputacional inaceptable'
    },
    
    'proveedor_confiable': {
        'descripcion': 'Proveedor altamente confiable',
        'condicion': lambda datos: (
            datos.get('calificacion_mercado', 0) >= UMBRALES_REPUTACIONALES['calificacion']['excelente'] and
            datos.get('incidentes_seguridad', 1) == 0 and
            datos.get('practicas_eticas', False) == True and
            datos.get('responsabilidad_ambiental', False) == True
        ),
        'impacto': -18,
        'categoria': 'reputacional',
        'severidad': 'positivo',
        'justificacion': 'Excelente reputación, sin incidentes y cumplimiento ESG integral indican proveedor de clase mundial'
    }
}

# Fuentes de información reputacional
FUENTES_INFORMACION = {
    'primarias': [
        'Referencias directas de clientes actuales',
        'Visitas a instalaciones',
        'Auditorías de terceros',
        'Entrevistas con personal clave'
    ],
    'secundarias': [
        'Calificaciones en plataformas B2B',
        'Redes sociales corporativas',
        'Noticias y artículos de prensa',
        'Reportes de sostenibilidad',
        'Bases de datos de proveedores'
    ],
    'registros_publicos': [
        'Sanciones regulatorias',
        'Demandas y litigios',
        'Listas de vigilancia (OFAC, ONU, etc.)',
        'Registros ambientales',
        'Certificaciones vigentes'
    ]
}

# Indicadores de reputación
INDICADORES_REPUTACION = {
    'calificacion_mercado': {
        'nombre': 'Calificación Promedio del Mercado',
        'escala': '1.0 - 5.0 estrellas',
        'descripcion': 'Promedio de calificaciones de clientes y mercado',
        'fuentes': ['Google Reviews', 'Trustpilot', 'LinkedIn', 'Plataformas B2B'],
        'ideal': '>= 4.5/5.0'
    },
    'incidentes_seguridad': {
        'nombre': 'Incidentes de Seguridad',
        'periodo': 'Últimos 24 meses',
        'tipos': [
            'Robos de carga',
            'Filtraciones de información',
            'Accidentes graves',
            'Contaminación de productos',
            'Incumplimientos de seguridad'
        ],
        'ideal': '0 incidentes'
    },
    'practicas_eticas': {
        'nombre': 'Prácticas Éticas y Cumplimiento',
        'aspectos': [
            'Código de ética documentado',
            'Políticas anti-corrupción',
            'Transparencia en operaciones',
            'No trabajo infantil',
            'No trabajo forzado',
            'Respeto a derechos humanos'
        ],
        'verificacion': 'Auditoría social o certificación SA 8000'
    },
    'responsabilidad_ambiental': {
        'nombre': 'Responsabilidad Ambiental',
        'criterios': CRITERIOS_ESG['ambiental'],
        'certificaciones': ['ISO 14001', 'FSC', 'Carbono Neutro'],
        'verificacion': 'Reportes de sostenibilidad y auditorías ambientales'
    }
}

# Banderas rojas reputacionales
RED_FLAGS_REPUTACIONALES = [
    'Calificaciones extremadamente bajas (<2.0/5.0)',
    'Múltiples quejas por calidad o servicio',
    'Escándalos públicos recientes',
    'Asociación con empresas sancionadas',
    'Cambios frecuentes de marca o razón social',
    'Presencia en medios por razones negativas',
    'Boicots o campañas en su contra',
    'Sanciones por violaciones ambientales',
    'Denuncias de explotación laboral',
    'Falta total de presencia digital verificable'
]

# Métricas de Net Promoter Score (NPS)
NPS_INTERPRETACION = {
    'promotores': {
        'rango': '9-10/10',
        'descripcion': 'Clientes altamente satisfechos que recomiendan activamente'
    },
    'pasivos': {
        'rango': '7-8/10',
        'descripcion': 'Clientes satisfechos pero no entusiastas'
    },
    'detractores': {
        'rango': '0-6/10',
        'descripcion': 'Clientes insatisfechos que pueden dañar la reputación'
    },
    'calculo': 'NPS = % Promotores - % Detractores',
    'interpretacion': {
        'excelente': '> 50',
        'bueno': '20-50',
        'aceptable': '0-20',
        'problematico': '< 0'
    }
}