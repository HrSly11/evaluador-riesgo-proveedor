"""
Sistema Experto para Evaluación de Riesgo de Proveedores
Aplicación Streamlit - Archivo Principal

"""

import streamlit as st

# Importar configuración y estilos
from ui.styles import aplicar_configuracion_pagina, aplicar_estilos

# Importar componentes de UI
from ui import (
    formulario_proveedor,
    mostrar_resultados,
    mostrar_pantalla_inicio,
    crear_banner
)

# Importar motor de inferencia
from engine import MotorEvaluacionRiesgo, DatosProveedor


# ========================================
# CONFIGURACIÓN INICIAL
# ========================================

# IMPORTANTE: Esta debe ser la PRIMERA llamada de Streamlit
aplicar_configuracion_pagina()

# Aplicar estilos CSS personalizados
aplicar_estilos()


# ========================================
# FUNCIONES AUXILIARES
# ========================================

def _ejecutar_evaluacion(datos: dict) -> dict:
    """Ejecuta la evaluación usando el motor de reglas"""
    
    motor = MotorEvaluacionRiesgo()
    motor.reset()

    # No mandar campos visuales al motor
    datos_motor = {k: v for k, v in datos.items() if k not in ['nombre', 'fecha_evaluacion']}

    motor.declare(DatosProveedor(**datos_motor))

    with st.spinner("🔄 Analizando proveedor... Por favor espera."):
        motor.run()

    return motor.obtener_resultado()


# ========================================
# FUNCIÓN PRINCIPAL
# ========================================

def main():
    crear_banner("Sistema Experto de Evaluación de Riesgo de Proveedores")

    datos = formulario_proveedor()

    if st.sidebar.button("🚀 Evaluar Proveedor", type="primary", use_container_width=True):
        resultado = _ejecutar_evaluacion(datos)
        st.session_state['resultado'] = resultado
        st.session_state['datos'] = datos
        mostrar_resultados(resultado, datos)

    elif 'resultado' in st.session_state and 'datos' in st.session_state:
        mostrar_resultados(st.session_state['resultado'], st.session_state['datos'])

    else:
        mostrar_pantalla_inicio()


# ========================================
# PUNTO DE ENTRADA
# ========================================

if __name__ == "__main__":
    main()