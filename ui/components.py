"""
Componentes Reutilizables de UI
Funciones para crear elementos visuales consistentes
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any


def crear_gauge_puntuacion(puntuacion: float) -> go.Figure:
    """
    Crea un gráfico tipo gauge para mostrar la puntuación de riesgo
    
    Args:
        puntuacion: Valor de 0 a 100
        
    Returns:
        Figura de Plotly con el gauge
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=puntuacion,
        title={'text': "Puntuación de Riesgo", 'font': {'size': 22}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#4e54c8"},
            'steps': [
                {'range': [0, 50], 'color': '#ffcdd2'},
                {'range': [50, 70], 'color': '#fff9c4'},
                {'range': [70, 100], 'color': '#c8e6c9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig


def crear_card_resultado(titulo: str, valor: str, color: str = '#000') -> None:
    """
    Crea una tarjeta de resultado con título y valor
    
    Args:
        titulo: Título de la tarjeta
        valor: Valor a mostrar
        color: Color del valor (hex o nombre)
    """
    st.markdown(f"""
    <div class='result-card'>
        <div class='result-title'>{titulo}</div>
        <div class='result-value' style='color:{color};'>{valor}</div>
    </div>
    """, unsafe_allow_html=True)


def crear_card_categoria(icono: str, titulo: str, descripcion: str) -> None:
    """
    Crea una tarjeta de categoría para la pantalla inicial
    
    Args:
        icono: Emoji del icono
        titulo: Título de la categoría
        descripcion: Descripción breve
    """
    st.markdown(f"""
    <div class='category-card'>
        <div class='category-icon'>{icono}</div>
        <div class='category-title'>{titulo}</div>
        <div class='category-text'>{descripcion}</div>
    </div>
    """, unsafe_allow_html=True)


def crear_rule_box(regla: str, razonamiento: str, impacto: str) -> None:
    """
    Crea una caja para mostrar una regla activada
    
    Args:
        regla: Nombre de la regla
        razonamiento: Explicación del razonamiento
        impacto: Descripción del impacto
    """
    st.markdown(f"""
    <div class='rule-box'>
        <b>{regla}</b><br>
        <i>{razonamiento}</i><br>
        <span style='color:#555;'>Impacto: {impacto}</span>
    </div>
    """, unsafe_allow_html=True)


def crear_banner(titulo: str) -> None:
    """
    Crea el banner principal de la aplicación
    
    Args:
        titulo: Título a mostrar en el banner
    """
    st.markdown(f"""
    <div class='banner'>
        <h1>{titulo}</h1>
    </div>
    """, unsafe_allow_html=True)


def crear_disclaimer(tipo: str = "responsabilidad") -> None:
    """
    Crea el disclaimer según el tipo especificado
    
    Args:
        tipo: Tipo de disclaimer ('responsabilidad', 'resultados', 'legal')
    """
    disclaimers = {
        'responsabilidad': """
        <div class='disclaimer'>
            ⚠️ <b>Descargo de Responsabilidad:</b><br>
            Esta herramienta es un asistente para la toma de decisiones. 
            La decisión final debe ser tomada por un humano calificado con autoridad 
            en la organización (Gerente de Compras, Comité de Riesgos, o Directorio 
            según el nivel de riesgo).
        </div>
        """,
        'resultados': """
        <div class='disclaimer'>
            ⚠️ <b>Descargo de responsabilidad en base al análisis de resultados:</b><br>
            Este sistema experto realiza una evaluación automatizada basada en reglas 
            predefinidas y datos ingresados por el usuario. Los resultados, puntuaciones 
            y recomendaciones deben interpretarse como un apoyo a la toma de decisiones,
            no como un dictamen financiero o legal definitivo. Se recomienda validar los 
            resultados con un análisis profesional adicional.
        </div>
        """,
        'legal': """
        <div class='disclaimer'>
            ⚠️ <b>Aviso Legal:</b><br>
            Este sistema NO reemplaza el juicio profesional, la due diligence completa, 
            ni las políticas internas de aprobación de proveedores de su organización.
            Los análisis deben ser validados por profesionales especializados antes de 
            tomar decisiones comerciales definitivas.
        </div>
        """
    }
    
    st.markdown(disclaimers.get(tipo, disclaimers['responsabilidad']), 
                unsafe_allow_html=True)


def crear_metrica_con_icono(icono: str, titulo: str, valor: str, 
                            delta: str = None, color: str = "#4e54c8") -> None:
    """
    Crea una métrica visual con icono
    
    Args:
        icono: Emoji del icono
        titulo: Título de la métrica
        valor: Valor principal
        delta: Cambio o información adicional
        color: Color del borde
    """
    delta_html = f"<div style='color: #666; font-size: 14px;'>{delta}</div>" if delta else ""
    
    st.markdown(f"""
    <div style='
        background: white;
        border: 2px solid {color};
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    '>
        <div style='font-size: 32px;'>{icono}</div>
        <div style='font-size: 14px; color: #666; margin: 0.5rem 0;'>{titulo}</div>
        <div style='font-size: 24px; font-weight: bold; color: #333;'>{valor}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def crear_seccion_titulo(titulo: str, icono: str = "") -> None:
    """
    Crea un título de sección con formato consistente
    
    Args:
        titulo: Texto del título
        icono: Emoji opcional para el título
    """
    st.markdown(f"""
    <div style='
        margin: 2rem 0 1rem 0;
        padding: 0.8rem 1rem;
        background: linear-gradient(90deg, #4e54c8, #8f94fb);
        border-radius: 8px;
        color: white;
    '>
        <h3 style='margin: 0; color: white;'>{icono} {titulo}</h3>
    </div>
    """, unsafe_allow_html=True)


def crear_alerta_nivel_riesgo(nivel: str, puntuacion: float) -> None:
    """
    Crea una alerta visual según el nivel de riesgo
    
    Args:
        nivel: Nivel de riesgo (BAJO, MODERADO, ALTO, CRÍTICO)
        puntuacion: Puntuación asociada
    """
    config = {
        'BAJO': {'color': '#4caf50', 'icono': '✅', 'tipo': 'success'},
        'MODERADO': {'color': '#ff9800', 'icono': '⚠️', 'tipo': 'warning'},
        'ALTO': {'color': '#f44336', 'icono': '🚨', 'tipo': 'error'},
        'CRÍTICO': {'color': '#b71c1c', 'icono': '🔴', 'tipo': 'error'}
    }
    
    info = config.get(nivel, config['MODERADO'])
    
    st.markdown(f"""
    <div style='
        background: {info['color']}15;
        border: 2px solid {info['color']};
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    '>
        <div style='font-size: 48px; text-align: center;'>{info['icono']}</div>
        <h2 style='text-align: center; color: {info['color']}; margin: 0.5rem 0;'>
            Nivel de Riesgo: {nivel}
        </h2>
        <p style='text-align: center; font-size: 18px; color: #333; margin: 0;'>
            Puntuación: {puntuacion:.0f}/100
        </p>
    </div>
    """, unsafe_allow_html=True)


def crear_separador() -> None:
    """Crea un separador visual entre secciones"""
    st.markdown("<hr style='margin: 2rem 0; border: 1px solid #e0e0e0;'>", 
                unsafe_allow_html=True)


def crear_badge(texto: str, color: str = "#4e54c8") -> str:
    """
    Crea un badge/etiqueta inline
    
    Args:
        texto: Texto del badge
        color: Color de fondo
        
    Returns:
        HTML del badge
    """
    return f"""
    <span style='
        background: {color};
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin: 0 0.2rem;
    '>{texto}</span>
    """