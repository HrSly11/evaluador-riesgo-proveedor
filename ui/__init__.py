"""
Paquete UI para el Sistema Experto de Evaluación de Riesgo de Proveedores
"""

from .styles import get_custom_css
from .components import (
    crear_gauge_puntuacion,
    crear_banner,
    crear_tarjeta_categoria,
    crear_tarjeta_resultado,
    crear_caja_regla,
    crear_disclaimer,
    crear_footer
)
from .formulario import formulario_proveedor
from .inicio import mostrar_inicio
from .resultados import mostrar_resultados

__all__ = [
    'get_custom_css',
    'crear_gauge_puntuacion',
    'crear_banner',
    'crear_tarjeta_categoria',
    'crear_tarjeta_resultado',
    'crear_caja_regla',
    'crear_disclaimer',
    'crear_footer',
    'formulario_proveedor',
    'mostrar_inicio',
    'mostrar_resultados'
]