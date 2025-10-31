"""
Módulo de Formulario
Componente del sidebar para captura de datos del proveedor
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any


def formulario_proveedor() -> Dict[str, Any]:
    """
    Crea el formulario en el sidebar para ingresar datos del proveedor
    
    Returns:
        Diccionario con todos los datos ingresados
    """
    st.sidebar.header("📝 Datos del Proveedor")
    
    datos = {}
    
    # ========== INFORMACIÓN GENERAL ==========
    st.sidebar.markdown("### 📋 Información General")
    datos['nombre'] = st.sidebar.text_input(
        "Nombre del Proveedor",
        "Proveedor XYZ S.A.",
        help="Razón social o nombre comercial del proveedor"
    )
    
    datos['industria'] = st.sidebar.selectbox(
        "Industria",
        ["manufactura", "servicios", "tecnología", "construcción", "logística"],
        help="Sector industrial al que pertenece el proveedor"
    )
    
    datos['tiempo_mercado'] = st.sidebar.number_input(
        "Años en el mercado",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5,
        help="Experiencia del proveedor en el mercado"
    )
    
    st.sidebar.markdown("---")
    
    # ========== INDICADORES FINANCIEROS ==========
    st.sidebar.markdown("### 💰 Indicadores Financieros")
    
    datos['liquidez_corriente'] = st.sidebar.slider(
        "Ratio de Liquidez Corriente",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        help="Activo Corriente / Pasivo Corriente. Ideal: ≥ 2.0"
    )
    
    datos['endeudamiento'] = st.sidebar.slider(
        "Nivel de Endeudamiento",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Pasivo Total / Activo Total. Ideal: < 0.4"
    )
    
    datos['rentabilidad'] = st.sidebar.slider(
        "Rentabilidad (%)",
        min_value=-50.0,
        max_value=50.0,
        value=10.0,
        step=1.0,
        help="Margen de utilidad neta. Ideal: ≥ 15%"
    ) / 100  # Convertir a decimal
    
    datos['historial_pagos'] = st.sidebar.slider(
        "Pagos Puntuales (%)",
        min_value=0.0,
        max_value=100.0,
        value=85.0,
        step=5.0,
        help="Porcentaje de pagos realizados a tiempo"
    )
    
    st.sidebar.markdown("---")
    
    # ========== INDICADORES OPERACIONALES ==========
    st.sidebar.markdown("### ⚙️ Indicadores Operacionales")
    
    datos['certificacion_calidad'] = st.sidebar.checkbox(
        "Certificación de Calidad (ISO 9001)",
        value=True,
        help="Cuenta con certificación ISO 9001 vigente"
    )
    
    datos['capacidad_produccion'] = st.sidebar.slider(
        "Capacidad de Producción (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=5.0,
        help="Utilización actual de la capacidad instalada"
    )
    
    datos['tasa_defectos'] = st.sidebar.slider(
        "Tasa de Defectos (%)",
        min_value=0.0,
        max_value=20.0,
        value=3.0,
        step=0.5,
        help="Porcentaje de productos defectuosos. Ideal: < 2%"
    )
    
    datos['cumplimiento_entregas'] = st.sidebar.slider(
        "Cumplimiento de Entregas (%)",
        min_value=0.0,
        max_value=100.0,
        value=90.0,
        step=5.0,
        help="Porcentaje de entregas realizadas a tiempo. Ideal: ≥ 95%"
    )
    
    st.sidebar.markdown("---")
    
    # ========== INDICADORES LEGALES ==========
    st.sidebar.markdown("### ⚖️ Indicadores Legales")
    
    datos['cumplimiento_legal'] = st.sidebar.checkbox(
        "Cumplimiento Legal Completo",
        value=True,
        help="Cumple con todas las regulaciones y normativas aplicables"
    )
    
    datos['certificacion_ambiental'] = st.sidebar.checkbox(
        "Certificación Ambiental (ISO 14001)",
        value=False,
        help="Cuenta con certificación ambiental ISO 14001"
    )
    
    datos['seguros_vigentes'] = st.sidebar.checkbox(
        "Seguros de Responsabilidad Vigentes",
        value=True,
        help="Mantiene pólizas de seguro actualizadas"
    )
    
    st.sidebar.markdown("---")
    
    # ========== INDICADORES REPUTACIONALES ==========
    st.sidebar.markdown("### ⭐ Indicadores Reputacionales")
    
    datos['calificacion_mercado'] = st.sidebar.slider(
        "Calificación de Mercado",
        min_value=1.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
        help="Calificación promedio de clientes (1-5 estrellas)"
    )
    
    datos['quejas_clientes'] = st.sidebar.number_input(
        "Quejas de Clientes (último año)",
        min_value=0,
        max_value=100,
        value=3,
        step=1,
        help="Número de quejas formales recibidas"
    )
    
    datos['referencias_positivas'] = st.sidebar.number_input(
        "Referencias Positivas Verificadas",
        min_value=0,
        max_value=20,
        value=5,
        step=1,
        help="Referencias comerciales positivas verificadas"
    )
    
    # ========== METADATA ==========
    datos['fecha_evaluacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return datos


def mostrar_resumen_datos(datos: Dict[str, Any]) -> None:
    """
    Muestra un resumen de los datos ingresados en el sidebar
    
    Args:
        datos: Diccionario con los datos del proveedor
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Resumen de Datos")
    
    # Calcular un indicador general rápido
    indicadores_positivos = sum([
        datos.get('liquidez_corriente', 0) >= 1.5,
        datos.get('endeudamiento', 1) <= 0.5,
        datos.get('rentabilidad', 0) >= 0.10,
        datos.get('certificacion_calidad', False),
        datos.get('cumplimiento_legal', False),
        datos.get('cumplimiento_entregas', 0) >= 90,
        datos.get('calificacion_mercado', 0) >= 4.0
    ])
    
    total_indicadores = 7
    porcentaje = (indicadores_positivos / total_indicadores) * 100
    
    st.sidebar.info(f"""
    **Indicadores Positivos:** {indicadores_positivos}/{total_indicadores}
    
    **Porcentaje:** {porcentaje:.0f}%
    
    ℹ️ *Esta es una evaluación preliminar. 
    Presiona "Evaluar Proveedor" para el análisis completo.*
    """)


def validar_datos(datos: Dict[str, Any]) -> tuple[bool, str]:
    """
    Valida que los datos ingresados sean correctos
    
    Args:
        datos: Diccionario con los datos del proveedor
        
    Returns:
        Tupla (es_valido, mensaje_error)
    """
    # Validar que el nombre no esté vacío
    if not datos.get('nombre') or datos['nombre'].strip() == "":
        return False, "⚠️ El nombre del proveedor es obligatorio"
    
    # Validar rangos numéricos
    if datos.get('liquidez_corriente', 0) < 0:
        return False, "⚠️ La liquidez corriente no puede ser negativa"
    
    if not (0 <= datos.get('endeudamiento', 0) <= 1):
        return False, "⚠️ El endeudamiento debe estar entre 0 y 1"
    
    if datos.get('tiempo_mercado', 0) < 0:
        return False, "⚠️ Los años en el mercado no pueden ser negativos"
    
    # Todo válido
    return True, "✅ Datos validados correctamente"