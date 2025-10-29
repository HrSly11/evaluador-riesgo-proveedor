"""
Paquete de Base de Conocimiento
Contiene las reglas de negocio organizadas por dominio
"""

from .reglas_financieras import REGLAS_FINANCIERAS, UMBRALES_FINANCIEROS
from .reglas_operacionales import REGLAS_OPERACIONALES, UMBRALES_OPERACIONALES
from .reglas_legales import REGLAS_LEGALES, CRITERIOS_LEGALES
from .reglas_reputacionales import REGLAS_REPUTACIONALES, UMBRALES_REPUTACIONALES

__all__ = [
    'REGLAS_FINANCIERAS',
    'UMBRALES_FINANCIEROS',
    'REGLAS_OPERACIONALES',
    'UMBRALES_OPERACIONALES',
    'REGLAS_LEGALES',
    'CRITERIOS_LEGALES',
    'REGLAS_REPUTACIONALES',
    'UMBRALES_REPUTACIONALES'
]

__version__ = '1.0.0'