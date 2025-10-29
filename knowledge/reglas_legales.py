"""
Reglas Legales y Normativas - Base de Conocimiento
Define las reglas para evaluar el cumplimiento legal de proveedores
"""

# Criterios legales críticos
CRITERIOS_LEGALES = {
    'demandas': {
        'sin_demandas': 0,
        'demandas_menores': 1,
        'demandas_moderadas': 2,
        'demandas_criticas': 3
    },
    'sanciones': {
        'sin_sanciones': 0,
        'sanciones_menores': 2,
        'sanciones_graves': 5
    }
}

# Documentos legales requeridos
DOCUMENTOS_REQUERIDOS = {
    'basicos': [
        'RUC o equivalente fiscal vigente',
        'Certificado de inscripción en registro mercantil',
        'Poderes vigentes de representantes legales'
    ],
    'tributarios': [
        'Certificado de cumplimiento tributario',
        'Declaraciones de impuestos actualizadas',
        'Sin deudas tributarias pendientes'
    ],
    'laborales': [
        'Planilla electrónica actualizada',
        'Pago de seguridad social al día',
        'Cumplimiento de beneficios laborales',
        'Sin demandas laborales graves'
    ],
    'permisos': [
        'Licencia municipal de funcionamiento',
        'Permisos sanitarios (si aplica)',
        'Permisos ambientales (si aplica)',
        'Certificados de Defensa Civil'
    ]
}

REGLAS_LEGALES = {
    'licencias_vigentes': {
        'descripcion': 'Todas las licencias y permisos están vigentes',
        'condicion': lambda datos: datos.get('licencias_vigentes', False) == True,
        'impacto': -5,
        'categoria': 'legal',
        'severidad': 'positivo',
        'justificacion': 'Licencias vigentes confirman que el proveedor opera legalmente según normativa local'
    },
    
    'licencias_vencidas': {
        'descripcion': 'Licencias o permisos vencidos',
        'condicion': lambda datos: datos.get('licencias_vigentes', True) == False,
        'impacto': 35,
        'categoria': 'legal',
        'severidad': 'critico',
        'justificacion': 'Operar sin licencias vigentes es ilegal y puede resultar en clausura, multas o paralización de operaciones'
    },
    
    'certificado_tributario_vigente': {
        'descripcion': 'Certificado tributario vigente',
        'condicion': lambda datos: datos.get('certificado_tributario', False) == True,
        'impacto': -5,
        'categoria': 'legal',
        'severidad': 'positivo',
        'justificacion': 'Certificado tributario vigente confirma que el proveedor está al día con sus obligaciones fiscales'
    },
    
    'problemas_tributarios': {
        'descripcion': 'Sin certificado tributario vigente',
        'condicion': lambda datos: datos.get('certificado_tributario', True) == False,
        'impacto': 20,
        'categoria': 'legal',
        'severidad': 'alto',
        'justificacion': 'Falta de certificado tributario sugiere deudas fiscales que pueden derivar en embargos o restricciones operativas'
    },
    
    'cumplimiento_laboral_ok': {
        'descripcion': 'Cumplimiento laboral verificado',
        'condicion': lambda datos: datos.get('cumplimiento_laboral', False) == True,
        'impacto': -5,
        'categoria': 'legal',
        'severidad': 'positivo',
        'justificacion': 'Cumplimiento laboral adecuado demuestra respeto por derechos de trabajadores y reduce riesgos de huelgas'
    },
    
    'incumplimiento_laboral': {
        'descripcion': 'Incumplimientos laborales detectados',
        'condicion': lambda datos: datos.get('cumplimiento_laboral', True) == False,
        'impacto': 28,
        'categoria': 'legal',
        'severidad': 'alto',
        'justificacion': 'Incumplimientos laborales pueden causar sanciones, huelgas, paralizaciones y daño reputacional'
    },
    
    'sin_demandas': {
        'descripcion': 'Sin demandas legales activas',
        'condicion': lambda datos: datos.get('demandas_legales', 1) == CRITERIOS_LEGALES['demandas']['sin_demandas'],
        'impacto': -10,
        'categoria': 'legal',
        'severidad': 'positivo',
        'justificacion': 'Ausencia de demandas indica buen cumplimiento normativo y relaciones comerciales saludables'
    },
    
    'demandas_menores': {
        'descripcion': 'Una demanda legal activa',
        'condicion': lambda datos: datos.get('demandas_legales', 0) == CRITERIOS_LEGALES['demandas']['demandas_menores'],
        'impacto': 8,
        'categoria': 'legal',
        'severidad': 'moderado',
        'justificacion': 'Una demanda activa requiere evaluación del tipo y monto para determinar riesgo real'
    },
    
    'demandas_moderadas': {
        'descripcion': 'Dos demandas legales activas',
        'condicion': lambda datos: datos.get('demandas_legales', 0) == CRITERIOS_LEGALES['demandas']['demandas_moderadas'],
        'impacto': 15,
        'categoria': 'legal',
        'severidad': 'alto',
        'justificacion': 'Múltiples demandas sugieren problemas recurrentes en cumplimiento de obligaciones'
    },
    
    'multiples_demandas': {
        'descripcion': 'Tres o más demandas legales activas',
        'condicion': lambda datos: datos.get('demandas_legales', 0) >= CRITERIOS_LEGALES['demandas']['demandas_criticas'],
        'impacto': 25,
        'categoria': 'legal',
        'severidad': 'critico',
        'justificacion': 'Múltiples demandas activas representan alto riesgo legal, financiero y reputacional'
    },
    
    'cumplimiento_legal_total': {
        'descripcion': 'Cumplimiento legal integral',
        'condicion': lambda datos: (
            datos.get('licencias_vigentes', False) == True and
            datos.get('certificado_tributario', False) == True and
            datos.get('cumplimiento_laboral', False) == True and
            datos.get('demandas_legales', 1) == 0
        ),
        'impacto': -15,
        'categoria': 'legal',
        'severidad': 'positivo',
        'justificacion': 'Cumplimiento total en todos los aspectos legales demuestra gestión corporativa responsable y de bajo riesgo'
    },
    
    'crisis_legal': {
        'descripcion': 'Crisis legal múltiple',
        'condicion': lambda datos: (
            datos.get('licencias_vigentes', True) == False and
            datos.get('certificado_tributario', True) == False and
            datos.get('demandas_legales', 0) >= CRITERIOS_LEGALES['demandas']['demandas_criticas']
        ),
        'impacto': 40,
        'categoria': 'legal',
        'severidad': 'critico',
        'justificacion': 'Múltiples problemas legales simultáneos indican alto riesgo de cierre, embargo o quiebra del proveedor'
    },
    
    'riesgo_legal_moderado': {
        'descripcion': 'Riesgo legal moderado',
        'condicion': lambda datos: (
            (datos.get('licencias_vigentes', True) == False or
             datos.get('certificado_tributario', True) == False or
             datos.get('cumplimiento_laboral', True) == False) and
            datos.get('demandas_legales', 0) <= 1
        ),
        'impacto': 12,
        'categoria': 'legal',
        'severidad': 'moderado',
        'justificacion': 'Algunos incumplimientos aislados requieren seguimiento pero son manejables con plan de acción'
    }
}

# Documentación de aspectos legales
DOCUMENTACION_LEGAL = {
    'licencias_vigentes': {
        'nombre': 'Licencias y Permisos',
        'descripcion': 'Autorizaciones legales necesarias para operar',
        'documentos_incluidos': DOCUMENTOS_REQUERIDOS['permisos'],
        'importancia': 'Sin licencias vigentes, el proveedor opera ilegalmente',
        'verificacion': 'Solicitar copias certificadas y verificar en registros públicos'
    },
    'certificado_tributario': {
        'nombre': 'Certificado de Cumplimiento Tributario',
        'descripcion': 'Documento que acredita estar al día con obligaciones fiscales',
        'vigencia': 'Generalmente 30-90 días',
        'importancia': 'Deudas tributarias pueden derivar en embargos de cuentas o activos',
        'verificacion': 'Solicitar certificado emitido por autoridad fiscal'
    },
    'cumplimiento_laboral': {
        'nombre': 'Cumplimiento Laboral',
        'aspectos': DOCUMENTOS_REQUERIDOS['laborales'],
        'importancia': 'Incumplimientos laborales causan huelgas, sanciones y multas',
        'verificacion': 'Revisar planilla electrónica, pago de CTS, vacaciones y beneficios'
    },
    'demandas_legales': {
        'nombre': 'Demandas y Litigios',
        'tipos': [
            'Demandas laborales',
            'Demandas comerciales',
            'Demandas civiles',
            'Procesos penales',
            'Sanciones administrativas'
        ],
        'importancia': 'Demandas activas pueden derivar en embargos, restricciones operativas o quiebra',
        'verificacion': 'Consultar registros judiciales y solicitar declaración jurada'
    }
}

# Niveles de due diligence legal recomendados
DUE_DILIGENCE_LEGAL = {
    'basico': {
        'alcance': 'Proveedores de bajo riesgo y montos menores',
        'verificaciones': [
            'RUC vigente',
            'Declaración jurada de cumplimiento legal',
            'Referencias comerciales'
        ]
    },
    'intermedio': {
        'alcance': 'Proveedores de riesgo moderado',
        'verificaciones': [
            'Certificado tributario vigente',
            'Búsqueda de demandas en registros públicos',
            'Verificación de licencias',
            'Referencias bancarias'
        ]
    },
    'exhaustivo': {
        'alcance': 'Proveedores críticos o alto riesgo',
        'verificaciones': [
            'Auditoría legal completa',
            'Revisión de contratos vigentes',
            'Análisis de contingencias legales',
            'Verificación de poderes y representación',
            'Historial de sanciones administrativas',
            'Due diligence en cadena de suministro'
        ]
    }
}

# Banderas rojas legales
RED_FLAGS_LEGALES = [
    'Negativa a proporcionar documentación legal',
    'Certificados vencidos o falsificados',
    'Múltiples cambios de razón social recientes',
    'Representantes legales sin poderes vigentes',
    'Domicilio fiscal inexistente o ficticio',
    'Aparición en listas de sanciones internacionales',
    'Historial de quiebras o concursos de acreedores',
    'Vínculo con empresas sancionadas',
    'Operaciones en paraísos fiscales sin justificación',
    'Negativa a auditorías o inspecciones'
]