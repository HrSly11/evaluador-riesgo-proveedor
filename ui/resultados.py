"""
Página de resultados de la evaluación
"""
import streamlit as st
import plotly.graph_objects as go
from engine.explicador import ExplicadorDecisiones
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

    # ========== RESUMEN EJECUTIVO ==========
    st.markdown("---")
    resumen_ejecutivo = explicador.generar_resumen_ejecutivo(resultado)
    st.markdown(resumen_ejecutivo)

    # ========== REGLAS ACTIVADAS ==========
    st.markdown("---")
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
        
        # ========== CADENA DE RAZONAMIENTO ==========
        st.markdown("---")
        cadena_razonamiento = explicador.generar_cadena_razonamiento(resultado['explicaciones'])
        st.markdown(cadena_razonamiento)
        
    else:
        st.info("No se activaron reglas específicas para este proveedor.")

    # ========== PLAN DE MITIGACIÓN ==========
    st.markdown("---")
    plan_mitigacion = explicador.generar_plan_mitigacion(resultado)
    st.markdown(plan_mitigacion)

    # ========== VISUALIZACIÓN DE MÉTRICAS ==========
    st.markdown("---")
    st.markdown("### 📊 Análisis por Categorías")
    
    metricas = explicador.generar_metricas_visuales(resultado)
    
    # Crear gráfico de barras para impacto por categoría
    if metricas['categorias']:
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.markdown("#### Impacto por Categoría")
            categorias_nombres = list(metricas['categorias'].keys())
            categorias_valores = list(metricas['categorias'].values())
            
            fig_categorias = go.Figure(data=[
                go.Bar(
                    x=categorias_nombres,
                    y=categorias_valores,
                    marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#feca57']
                )
            ])
            fig_categorias.update_layout(
                xaxis_title="Categoría",
                yaxis_title="Puntos de Impacto Negativo",
                height=300,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_categorias, use_container_width=True)
        
        with col_viz2:
            st.markdown("#### Distribución de Alertas")
            alertas = metricas['alertas_por_nivel']
            
            if sum(alertas.values()) > 0:
                fig_alertas = go.Figure(data=[
                    go.Pie(
                        labels=list(alertas.keys()),
                        values=list(alertas.values()),
                        marker_colors=['#ff6b6b', '#feca57', '#45b7d1']
                    )
                ])
                fig_alertas.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=30, b=20)
                )
                st.plotly_chart(fig_alertas, use_container_width=True)
            else:
                st.info("No hay alertas registradas para este proveedor.")

    # ========== DESCARGA DE INFORME ==========
    st.markdown("---")

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