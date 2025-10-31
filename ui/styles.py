"""
Módulo de Estilos CSS para la aplicación Streamlit
Centraliza todos los estilos personalizados
"""

import streamlit as st


def aplicar_estilos():
    """
    Aplica los estilos CSS personalizados a la aplicación Streamlit
    """
    st.markdown("""
    <style>
        /* ========== ESTILOS GENERALES ========== */
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #4e54c8 0%, #8f94fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .banner {
            text-align: center;
            background: linear-gradient(90deg, #4e54c8, #8f94fb);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        /* ========== DISCLAIMER ========== */
        .disclaimer {
            background-color: #e3f2fd;
            border: 2px solid #2196f3;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 2rem 0;
            color: #000000;
        }
        .disclaimer b {
            color: #1565c0;
        }

        /* ========== CUADROS DE RESULTADOS ========== */
        .result-card {
            background: #ffffff;
            border: 2px solid #4e54c8;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            color: #333333;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .result-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 0.8rem;
            color: #4e54c8;
        }
        .result-value {
            font-size: 24px;
            font-weight: bold;
            color: #000;
        }

        /* ========== TARJETAS DE CATEGORÍAS ========== */
        .category-card {
            background: white;
            border: 2px solid #4e54c8;
            border-radius: 12px;
            padding: 1.2rem;
            text-align: center;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s ease-in-out;
        }
        .category-card:hover {
            transform: scale(1.03);
            background: #f8f9ff;
        }
        .category-icon {
            font-size: 32px;
            margin-bottom: 0.5rem;
        }
        .category-title {
            font-weight: bold;
            font-size: 17px;
            margin-bottom: 8px;
            color: #4e54c8;
        }
        .category-text {
            font-size: 14px;
            color: #333;
            line-height: 1.4;
        }

        /* ========== REGLAS ACTIVADAS ========== */
        .rule-box {
            background-color: #f9f9f9;
            border-left: 5px solid #4e54c8;
            padding: 0.7rem 1rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            color: #000000;
        }
        .rule-box b {
            color: #222;
        }
        .rule-box i {
            color: #333;
        }
        
        /* ========== ESPACIADO ========== */
        .stMarkdown > div:has(.instructions-block) {
            margin-top: 2.5rem !important;
        }
        
        .stDownloadButton {
            margin-top: 1.5rem !important;
            margin-bottom: 1.5rem !important;
        }

        /* ========== AJUSTES DE SIDEBAR ========== */
        .css-1d391kg {
            padding-top: 1rem;
        }

        /* ========== BOTONES ========== */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
    </style>
    """, unsafe_allow_html=True)


def aplicar_configuracion_pagina():
    """
    Configura los parámetros iniciales de la página Streamlit
    """
    st.set_page_config(
        page_title="Evaluador de Riesgo de Proveedores",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "Sistema Experto de Evaluación de Riesgo de Proveedores v1.0"
        }
    )