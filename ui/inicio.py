"""
Página de inicio de la aplicación
"""
import streamlit as st
from ui.components import crear_tarjeta_categoria, crear_footer


def mostrar_inicio():
    """Muestra la página de inicio con información general del sistema"""
    
    st.markdown("<h2 style='text-align:center;'>🏠 Bienvenido</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <p style='text-align:center; font-size:17px;'>
    Este sistema experto analiza proveedores en 4 dimensiones: <b>Financiera</b>, <b>Operacional</b>, <b>Legal</b> y <b>Reputacional</b>.
    Utiliza un motor de inferencia basado en reglas y proporciona trazabilidad completa de las decisiones.
    </p>
    """, unsafe_allow_html=True)

    # Mostrar las 4 categorías
    colA, colB, colC, colD = st.columns(4)
    
    with colA:
        st.markdown(
            crear_tarjeta_categoria(
                "💰", 
                "Financiero", 
                "Liquidez, endeudamiento y rentabilidad"
            ), 
            unsafe_allow_html=True
        )
    
    with colB:
        st.markdown(
            crear_tarjeta_categoria(
                "⚙️", 
                "Operacional", 
                "Capacidad, entregas y calidad"
            ), 
            unsafe_allow_html=True
        )
    
    with colC:
        st.markdown(
            crear_tarjeta_categoria(
                "⚖️", 
                "Legal", 
                "Cumplimiento normativo y seguros"
            ), 
            unsafe_allow_html=True
        )
    
    with colD:
        st.markdown(
            crear_tarjeta_categoria(
                "🌐", 
                "Reputacional", 
                "Reputación, quejas y referencias"
            ), 
            unsafe_allow_html=True
        )

    # Espaciado
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
    
    # Instrucciones
    st.info("""
    **Instrucciones:**
    
    1️⃣ Completa los datos del proveedor en el menú lateral.
      
    2️⃣ Presiona **"🚀 Evaluar Proveedor"**.
      
    3️⃣ Visualiza el resultado y descarga el informe generado.
    """)

    # Footer
    st.markdown(crear_footer(), unsafe_allow_html=True)