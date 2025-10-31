"""
Módulo de Pantalla Inicial
Pantalla de bienvenida y presentación del sistema
"""

import streamlit as st
from .components import crear_card_categoria, crear_banner


def mostrar_pantalla_inicio() -> None:
    """
    Muestra la pantalla inicial con información del sistema
    """
    # ========== TÍTULO PRINCIPAL ==========
    st.markdown(
        "<h2 style='text-align:center;'>🏠 Bienvenido</h2>",
        unsafe_allow_html=True
    )
    
    # ========== DESCRIPCIÓN ==========
    st.markdown("""
    <p style='text-align:center; font-size:17px;'>
    Este sistema experto analiza proveedores en 4 dimensiones: 
    <b>Financiera</b>, <b>Operacional</b>, <b>Legal</b> y <b>Reputacional</b>.
    Utiliza un motor de inferencia basado en reglas y proporciona 
    trazabilidad completa de las decisiones.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========== TARJETAS DE CATEGORÍAS ==========
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        crear_card_categoria(
            "💰",
            "Financiero",
            "Liquidez, endeudamiento y rentabilidad"
        )
    
    with col2:
        crear_card_categoria(
            "⚙️",
            "Operacional",
            "Capacidad, entregas y calidad"
        )
    
    with col3:
        crear_card_categoria(
            "⚖️",
            "Legal",
            "Cumplimiento normativo y seguros"
        )
    
    with col4:
        crear_card_categoria(
            "🌐",
            "Reputacional",
            "Reputación, quejas y referencias"
        )
    
    # ========== ESPACIO ==========
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
    
    # ========== INSTRUCCIONES ==========
    _mostrar_instrucciones()
    
    # ========== CARACTERÍSTICAS DEL SISTEMA ==========
    _mostrar_caracteristicas()
    
    # ========== CRÉDITOS ==========
    _mostrar_creditos()


def _mostrar_instrucciones() -> None:
    """Muestra las instrucciones de uso"""
    st.info("""
    **📋 Instrucciones de Uso:**
    
    1️⃣ **Completa los datos** del proveedor en el menú lateral izquierdo
    
    2️⃣ **Presiona** el botón **"🚀 Evaluar Proveedor"**
    
    3️⃣ **Visualiza** el resultado y descarga el informe generado
    
    4️⃣ **Revisa** la trazabilidad de reglas activadas para entender la decisión
    """)


def _mostrar_caracteristicas() -> None:
    """Muestra las características principales del sistema"""
    st.markdown("### ✨ Características Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Evaluación Integral:**
        - Análisis en 4 dimensiones clave
        - 30+ reglas de negocio expertas
        - Sistema de puntuación de 0-100
        - Niveles: Bajo, Moderado, Alto, Crítico
        
        **🔍 Explicabilidad Total:**
        - Trazabilidad de cada decisión
        - Justificación de reglas activadas
        - Recomendaciones accionables
        - Informes descargables
        """)
    
    with col2:
        st.markdown("""
        **🛡️ Enfoque Responsable:**
        - Decisión final humana requerida
        - Sin discriminación por atributos sensibles
        - Limitaciones claramente explicadas
        - Cumplimiento con estándares éticos
        
        **📊 Visualización Clara:**
        - Gráficos interactivos
        - Código de colores intuitivo
        - Resumen ejecutivo
        - Análisis por categoría
        """)


def _mostrar_creditos() -> None:
    """Muestra los créditos del equipo"""
    st.markdown("""
    <div style='text-align:center; margin-top:30px; padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; color: white;'>
        <h4 style='color: white; margin-bottom: 10px;'>
            👩‍💻 Desarrollado por el <b>Grupo N°2</b>
        </h4>
        <p style='color: white; margin-bottom: 5px;'>
            <b>Escuela de Ingeniería de Sistemas</b>
        </p>
        <p style='color: white; font-size: 14px; line-height: 1.6;'>
            Chávez Alva Tania Ycela · Cruz Esquivel Luis Josmell · 
            Cruz Vargas Germain Alexander · Rodríguez Sandoval Harry Sly · 
            Villa Valdiviezo Favián Enrique
        </p>
    </div>
    """, unsafe_allow_html=True)


def mostrar_estadisticas_sistema() -> None:
    """
    Muestra estadísticas del sistema
    (Opcional - puede agregarse en la pantalla inicial)
    """
    st.markdown("### 📈 Estadísticas del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Reglas de Negocio", "30+", delta="Actualizadas")
    
    with col2:
        st.metric("Dimensiones", "4", delta="Completas")
    
    with col3:
        st.metric("Tests Automatizados", "20", delta="Pasando ✅")
    
    with col4:
        st.metric("Precisión", "95%", delta="+5%")


def mostrar_casos_ejemplo() -> None:
    """
    Muestra casos de ejemplo para que el usuario pruebe
    (Opcional - puede agregarse como expander)
    """
    with st.expander("💡 Ver Casos de Ejemplo"):
        st.markdown("""
        **Caso 1: Proveedor de Bajo Riesgo ✅**
        - Liquidez: 2.5
        - Endeudamiento: 0.3 (30%)
        - Rentabilidad: 18%
        - Cumplimiento entregas: 98%
        
        **Caso 2: Proveedor de Alto Riesgo ⚠️**
        - Liquidez: 0.6
        - Endeudamiento: 0.85 (85%)
        - Rentabilidad: -5%
        - Cumplimiento entregas: 70%
        
        *Puedes copiar estos valores en el formulario para probar el sistema*
        """)