"""
Página de resultados de la evaluación
"""
import streamlit as st
from engine import ExplicadorDecisiones
from ui.components import (
    crear_gauge_puntuacion, 
    crear_tarjeta_resultado, 
    crear_caja_regla,
    crear_disclaimer
)


def mostrar_resultados(resultado, datos):
    """
    Muestra los resultados de la evaluación de riesgo
    
    Args:
        resultado: Diccionario con los resultados de la evaluación
        datos: Diccionario con los datos del proveedor evaluado
    """
    explicador = ExplicadorDecisiones()
    
    st.markdown("## 📈 Resultados de la Evaluación")

    # Crear las 3 tarjetas de resumen
    col1, col2, col3 = st.columns(3)
    
    # Definir colores según el nivel de riesgo
    colores_riesgo = {
        'BAJO': 'green', 
        'MODERADO': 'orange', 
        'ALTO': 'red', 
        'CRÍTICO': '#b71c1c'
    }
    color = colores_riesgo.get(resultado['riesgo_final'], 'gray')

    with col1:
        st.markdown(
            crear_tarjeta_resultado(
                "Nivel de Riesgo", 
                resultado['riesgo_final'], 
                color
            ), 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            crear_tarjeta_resultado(
                "Puntuación", 
                f"{resultado['puntuacion']:.0f}/100"
            ), 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            crear_tarjeta_resultado(
                "Reglas Activadas", 
                str(resultado['total_reglas_activadas'])
            ), 
            unsafe_allow_html=True
        )

    # Espaciado
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    # Mostrar gauge de puntuación
    st.plotly_chart(
        crear_gauge_puntuacion(resultado['puntuacion']), 
        use_container_width=True
    )

    # Mostrar recomendación
    if resultado['riesgo_final'] in ['BAJO', 'MODERADO']:
        st.success(resultado['recomendacion'])
    else:
        st.warning(resultado['recomendacion'])

    # Mostrar reglas activadas y explicaciones
    if resultado.get('explicaciones'):
        st.markdown("### ⚙️ Reglas Activadas y Explicaciones")
        
        for exp in resultado['explicaciones']:
            st.markdown(
                crear_caja_regla(
                    exp['regla'],
                    exp['razonamiento'],
                    exp['impacto']
                ), 
                unsafe_allow_html=True
            )
    else:
        st.info("No se activaron reglas específicas para este proveedor.")

    # Botón de descarga del informe
    informe_md = explicador.generar_informe_completo(resultado, datos)
    st.download_button(
        label="⬇️ Descargar informe...",
        data=informe_md,
        file_name=f"informe_{datos['nombre'].replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True
    )

    # Disclaimer
    st.markdown(crear_disclaimer(), unsafe_allow_html=True)

    # Botón para nueva evaluación
    if st.button("🔁 Hacer una nueva evaluación...", use_container_width=True):
        st.session_state.clear()
        st.rerun()