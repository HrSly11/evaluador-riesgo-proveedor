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
# FUNCIÓN PRINCIPAL
# ========================================

def main():
    """
    Función principal que orquesta la aplicación
    """
    
    # ========== BANNER PRINCIPAL ==========
    crear_banner("Sistema Experto de Evaluación de Riesgo de Proveedores")
    
    # ========== FORMULARIO EN SIDEBAR ==========
    datos = formulario_proveedor()
    
    # ========== BOTÓN DE EVALUACIÓN ==========
    if st.sidebar.button("🚀 Evaluar Proveedor", type="primary", use_container_width=True):
        # Realizar evaluación
        resultado = _ejecutar_evaluacion(datos)
        
        # Guardar en session state
        st.session_state['resultado'] = resultado
        st.session_state['datos'] = datos
        
        # Mostrar resultados
        mostrar_resultados(resultado, datos)
    
    # ========== MOSTRAR RESULTADOS PREVIOS ==========
    elif 'resultado' in st.session_state and 'datos' in st.session_state:
        mostrar_resultados(
            st.session_state['resultado'],
            st.session_state['datos']
        )
    
    # ========== PANTALLA INICIAL ==========
    else:
        mostrar_pantalla_inicio()


# ========================================
# FUNCIONES AUXILIARES
# ========================================

def _ejecutar_evaluacion(datos: dict) -> dict:
    """
    Ejecuta la evaluación del proveedor usando el motor de inferencia
    
    Args:
        datos: Diccionario con los datos del proveedor
        
    Returns:
        Diccionario con los resultados de la evaluación
    """
    # Crear instancia del motor
    motor = MotorEvaluacionRiesgo()
    motor.reset()
    
    # Filtrar datos para el motor (excluir metadata)
    datos_motor = {
        k: v for k, v in datos.items() 
        if k not in ['nombre', 'fecha_evaluacion']
    }
    
    # Declarar hechos
    motor.declare(DatosProveedor(**datos_motor))
    
    # Ejecutar motor de inferencia con spinner
    with st.spinner("🔄 Analizando proveedor... Por favor espera."):
        motor.run()
    
    # Obtener resultado
    resultado = motor.obtener_resultado()
    
    return resultado


# ========================================
# PUNTO DE ENTRADA
# ========================================

if __name__ == "__main__":
    main()