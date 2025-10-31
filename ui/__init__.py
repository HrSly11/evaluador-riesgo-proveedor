"""
Paquete UI - Componentes de Interfaz Streamlit
Separación de componentes visuales según arquitectura solicitada
"""

from .styles import aplicar_estilos
from .components import (
    crear_gauge_puntuacion,
    crear_card_resultado,
    crear_card_categoria,
    crear_rule_box,
    crear_banner,
    crear_disclaimer
)
from .formulario import formulario_proveedor
from .resultados import mostrar_resultados
from .inicio import mostrar_pantalla_inicio

__all__ = [
    'aplicar_estilos',
    'crear_gauge_puntuacion',
    'crear_card_resultado',
    'crear_card_categoria',
    'crear_rule_box',
    'crear_banner',
    'crear_disclaimer',
    'formulario_proveedor',
    'mostrar_resultados',
    'mostrar_pantalla_inicio'
]

__version__ = '1.0.0'