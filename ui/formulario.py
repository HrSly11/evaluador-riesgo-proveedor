"""
Formulario de entrada de datos del proveedor
"""
import streamlit as st
from datetime import datetime


def formulario_proveedor():
    """
    Renderiza el formulario del sidebar para ingresar datos del proveedor
    
    Returns:
        dict: Diccionario con todos los datos ingresados del proveedor
    """
    st.sidebar.header("📝 Datos del Proveedor")

    datos = {}

    # ====== Sección General ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("📌 Información General")
    
    datos['nombre'] = st.sidebar.text_input(
        "Nombre del Proveedor", 
        "Proveedor XYZ S.A."
    )
    
    datos['industria'] = st.sidebar.selectbox(
        "Industria",
        [
            "Manufactura", "Servicios", "Tecnología", "Construcción", "Logística",
            "Agricultura", "Minería", "Salud", "Educación", "Retail", "Energía",
            "Transporte", "Finanzas", "Turismo", "Textil"
        ],
        help="Selecciona el sector al que pertenece el proveedor."
    )
    
    datos['tiempo_mercado'] = st.sidebar.number_input(
        "Años en el mercado", 
        0.0, 
        100.0, 
        5.0, 
        0.5
    )

    # ====== Sección Financiera ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Indicadores Financieros")
    
    datos['liquidez_corriente'] = st.sidebar.slider(
        "Ratio de Liquidez Corriente", 
        0.0, 
        5.0, 
        1.5, 
        0.1
    )
    
    datos['endeudamiento'] = st.sidebar.slider(
        "Nivel de Endeudamiento", 
        0.0, 
        1.0, 
        0.5, 
        0.05
    )
    
    datos['rentabilidad'] = st.sidebar.slider(
        "Rentabilidad (%)", 
        -50.0, 
        50.0, 
        10.0, 
        1.0
    ) / 100
    
    datos['historial_pagos'] = st.sidebar.slider(
        "Pagos Puntuales (%)", 
        0.0, 
        100.0, 
        85.0, 
        5.0
    )

    # ====== Sección Operacional ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Indicadores Operacionales")
    
    datos['certificacion_calidad'] = st.sidebar.checkbox(
        "Certificación de Calidad (ISO 9001)", 
        True
    )
    
    datos['capacidad_produccion'] = st.sidebar.slider(
        "Capacidad de Producción (%)", 
        0.0, 
        100.0, 
        75.0, 
        5.0
    )
    
    datos['tasa_defectos'] = st.sidebar.slider(
        "Tasa de Defectos (%)", 
        0.0, 
        20.0, 
        3.0, 
        0.5
    )
    
    datos['cumplimiento_entregas'] = st.sidebar.slider(
        "Cumplimiento de Entregas (%)", 
        0.0, 
        100.0, 
        90.0, 
        5.0
    )

    # ====== Sección Legal ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚖️ Indicadores Legales")
    
    datos['cumplimiento_legal'] = st.sidebar.checkbox(
        "Cumplimiento Legal Completo", 
        True
    )
    
    datos['certificacion_ambiental'] = st.sidebar.checkbox(
        "Certificación Ambiental (ISO 14001)", 
        False
    )
    
    datos['seguros_vigentes'] = st.sidebar.checkbox(
        "Seguros de Responsabilidad Vigentes", 
        True
    )

    # ====== Sección Reputacional ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("⭐ Indicadores Reputacionales")
    
    datos['calificacion_mercado'] = st.sidebar.slider(
        "Calificación de Mercado", 
        1.0, 
        5.0, 
        4.0, 
        0.1
    )
    
    datos['quejas_clientes'] = st.sidebar.number_input(
        "Quejas de Clientes (último año)", 
        0, 
        100, 
        3
    )
    
    datos['referencias_positivas'] = st.sidebar.number_input(
        "Referencias Positivas Verificadas", 
        0, 
        20, 
        5
    )

    # Agregar fecha de evaluación
    datos['fecha_evaluacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return datos