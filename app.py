import streamlit as st
import fix_collections  # ← AÑADE ESTA LÍNEA AQUÍ (ANTES de los demás imports)

# Ahora sí puedes importar engine
from engine import MotorEvaluacionRiesgo, DatosProveedor, ExplicadorDecisiones

# ... resto de tu código
"""
Sistema Experto de Evaluación de Riesgo de Proveedores
Aplicación principal con interfaz Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from engine import MotorEvaluacionRiesgo, DatosProveedor, ExplicadorDecisiones

# Configuración de la página
st.set_page_config(
    page_title="Evaluador de Riesgo de Proveedores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .alert-critico {
        background-color: #fee;
        border-left: 5px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .alert-alto {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .alert-medio {
        background-color: #fff9c4;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .disclaimer {
        background-color: #e3f2fd;
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 2rem 0;
    }
    
    .success-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def crear_gauge_puntuacion(puntuacion: float):
    """Crea un gráfico de gauge para la puntuación"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=puntuacion,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Puntuación de Riesgo", 'font': {'size': 24}},
        delta={'reference': 80, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffcdd2'},
                {'range': [50, 70], 'color': '#fff9c4'},
                {'range': [70, 100], 'color': '#c8e6c9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 60
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def crear_grafico_categorias(metricas: dict):
    """Crea gráfico de barras de impacto por categoría"""
    categorias = metricas['categorias']
    
    df = pd.DataFrame({
        'Categoría': list(categorias.keys()),
        'Impacto': list(categorias.values())
    })
    
    fig = px.bar(
        df,
        x='Categoría',
        y='Impacto',
        title='Impacto en Puntuación por Categoría de Riesgo',
        color='Impacto',
        color_continuous_scale=['green', 'yellow', 'red']
    )
    
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    return fig


def crear_grafico_alertas(metricas: dict):
    """Crea gráfico de dona de alertas por nivel"""
    alertas = metricas['alertas_por_nivel']
    
    labels = list(alertas.keys())
    values = list(alertas.values())
    colors = ['#f44336', '#ff9800', '#ffc107']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title='Distribución de Alertas por Nivel',
        height=400
    )
    
    return fig


def mostrar_header():
    """Muestra el encabezado de la aplicación"""
    st.markdown('<h1 class="main-header">📊 Sistema Experto de Evaluación de Riesgo</h1>', 
                unsafe_allow_html=True)
    st.markdown("### Evaluación Integral de Proveedores")
    
    st.markdown("""
    <div class="disclaimer">
        <h4>⚠️ AVISO IMPORTANTE</h4>
        <p><strong>Esta herramienta es un sistema de asistencia a la decisión.</strong></p>
        <p>La evaluación final y la decisión de contratación DEBE ser realizada por:</p>
        <ul>
            <li>Personal calificado del área de compras</li>
            <li>Gerentes de cadena de suministro</li>
            <li>Comité de evaluación de proveedores</li>
        </ul>
        <p><em>Este sistema NO reemplaza el criterio profesional humano ni la due diligence completa.</em></p>
    </div>
    """, unsafe_allow_html=True)


def formulario_proveedor():
    """Muestra el formulario para ingresar datos del proveedor"""
    st.sidebar.header("📝 Datos del Proveedor")
    
    datos = {}
    
    # Información general
    st.sidebar.subheader("Información General")
    datos['nombre'] = st.sidebar.text_input("Nombre del Proveedor", "Proveedor XYZ S.A.")
    datos['industria'] = st.sidebar.selectbox(
        "Industria",
        ["manufactura", "servicios", "tecnología", "construcción", "logística"]
    )
    datos['tiempo_mercado'] = st.sidebar.number_input(
        "Años en el mercado",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5
    )
    
    # Indicadores Financieros
    st.sidebar.subheader("💰 Indicadores Financieros")
    datos['liquidez_corriente'] = st.sidebar.slider(
        "Ratio de Liquidez Corriente",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        help="Activos corrientes / Pasivos corrientes"
    )
    
    datos['endeudamiento'] = st.sidebar.slider(
        "Nivel de Endeudamiento",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Pasivo total / Activo total"
    )
    
    datos['rentabilidad'] = st.sidebar.slider(
        "Rentabilidad (%)",
        min_value=-50.0,
        max_value=50.0,
        value=10.0,
        step=1.0,
        help="ROE o margen neto"
    ) / 100
    
    datos['historial_pagos'] = st.sidebar.slider(
        "Pagos Puntuales (%)",
        min_value=0.0,
        max_value=100.0,
        value=85.0,
        step=5.0,
        help="Porcentaje de pagos realizados a tiempo"
    )
    
    # Indicadores Operacionales
    st.sidebar.subheader("⚙️ Indicadores Operacionales")
    datos['certificacion_calidad'] = st.sidebar.checkbox(
        "Certificación de Calidad (ISO 9001)",
        value=True
    )
    
    datos['capacidad_produccion'] = st.sidebar.slider(
        "Capacidad de Producción (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=5.0,
        help="Porcentaje de capacidad instalada utilizable"
    )
    
    datos['tasa_defectos'] = st.sidebar.slider(
        "Tasa de Defectos (%)",
        min_value=0.0,
        max_value=20.0,
        value=3.0,
        step=0.5
    )
    
    datos['cumplimiento_entregas'] = st.sidebar.slider(
        "Cumplimiento de Entregas (%)",
        min_value=0.0,
        max_value=100.0,
        value=90.0,
        step=5.0
    )
    
    # Indicadores Legales
    st.sidebar.subheader("⚖️ Indicadores Legales")
    datos['cumplimiento_legal'] = st.sidebar.checkbox(
        "Cumplimiento Legal Completo",
        value=True,
        help="Sin antecedentes de incumplimiento normativo"
    )
    
    datos['certificacion_ambiental'] = st.sidebar.checkbox(
        "Certificación Ambiental (ISO 14001)",
        value=False
    )
    
    datos['seguros_vigentes'] = st.sidebar.checkbox(
        "Seguros de Responsabilidad Vigentes",
        value=True
    )
    
    # Indicadores Reputacionales
    st.sidebar.subheader("⭐ Indicadores Reputacionales")
    datos['calificacion_mercado'] = st.sidebar.slider(
        "Calificación de Mercado",
        min_value=1.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
        help="Calificación promedio de clientes"
    )
    
    datos['quejas_clientes'] = st.sidebar.number_input(
        "Quejas de Clientes (último año)",
        min_value=0,
        max_value=100,
        value=3,
        step=1
    )
    
    datos['referencias_positivas'] = st.sidebar.number_input(
        "Referencias Positivas Verificadas",
        min_value=0,
        max_value=20,
        value=5,
        step=1
    )
    
    datos['fecha_evaluacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return datos


def ejecutar_evaluacion(datos: dict):
    """Ejecuta la evaluación del proveedor"""
    # Crear motor de inferencia
    motor = MotorEvaluacionRiesgo()
    motor.reset()
    
    # Declarar hechos
    motor.declare(DatosProveedor(**{k: v for k, v in datos.items() 
                                    if k not in ['nombre', 'fecha_evaluacion']}))
    
    # Ejecutar motor
    with st.spinner('🔄 Evaluando proveedor...'):
        motor.run()
    
    # Obtener resultados
    resultado = motor.obtener_resultado()
    
    return resultado


def mostrar_resultados(resultado: dict, datos: dict):
    """Muestra los resultados de la evaluación"""
    explicador = ExplicadorDecisiones()
    
    # Resumen Ejecutivo
    st.markdown("## 📈 Resumen Ejecutivo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        riesgo = resultado['riesgo_final']
        color_riesgo = {
            'BAJO': 'green',
            'MEDIO': 'orange',
            'ALTO': 'red'
        }
        st.markdown(f"""
        <div style="background-color: {color_riesgo.get(riesgo, 'gray')}; 
                    padding: 2rem; border-radius: 10px; text-align: center;">
            <h2 style="color: white; margin: 0;">Riesgo {riesgo}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(
            label="Puntuación Final",
            value=f"{resultado['puntuacion']:.0f}/100",
            delta=f"{resultado['puntuacion'] - 60:.0f} vs mínimo aceptable"
        )
    
    with col3:
        st.metric(
            label="Reglas Activadas",
            value=resultado['total_reglas_activadas'],
            delta=f"{len(resultado['factores_criticos'])} críticos"
        )
    
    # Gráfico de puntuación
    st.plotly_chart(crear_gauge_puntuacion(resultado['puntuacion']), 
                    use_container_width=True)
    
    # Recomendación
    st.markdown("## 💡 Recomendación")
    if resultado['riesgo_final'] == 'BAJO':
        st.markdown(f'<div class="success-box"><h3>✅ {resultado["recomendacion"]}</h3></div>', 
                   unsafe_allow_html=True)
    else:
        st.warning(f"**{resultado['recomendacion']}**")
    
    # Alertas
    if resultado['alertas']:
        st.markdown("## 🚨 Alertas Identificadas")
        for alerta in resultado['alertas']:
            nivel = alerta['nivel']
            clase = f"alert-{nivel.lower()}"
            st.markdown(f"""
            <div class="{clase}">
                <strong>{nivel}:</strong> {alerta['mensaje']}
            </div>
            """, unsafe_allow_html=True)
    
    # Visualizaciones
    st.markdown("## 📊 Análisis Detallado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metricas = explicador.generar_metricas_visuales(resultado)
        st.plotly_chart(crear_grafico_categorias(metricas), 
                       use_container_width=True)
    
    with col2:
        if resultado['alertas']:
            st.plotly_chart(crear_grafico_alertas(metricas), 
                           use_container_width=True)
    
    # Trazabilidad - Reglas Activadas
    st.markdown("## 🔍 Trazabilidad: Reglas Activadas")
    st.markdown("""
    Esta sección muestra **exactamente cómo el sistema llegó a su conclusión**, 
    detallando cada regla que se activó durante la evaluación.
    """)
    
    if resultado['explicaciones']:
        df_explicaciones = explicador.generar_explicacion_detallada(resultado['explicaciones'])
        st.dataframe(
            df_explicaciones,
            use_container_width=True,
            hide_index=True
        )
        
        # Cadena de razonamiento
        with st.expander("📖 Ver Cadena de Razonamiento Completa"):
            st.markdown(explicador.generar_cadena_razonamiento(resultado['explicaciones']))
    else:
        st.success("✅ No se identificaron problemas críticos. Todas las métricas están dentro de rangos aceptables.")
    
    # Plan de Mitigación
    st.markdown("## 🔧 Plan de Mitigación")
    st.markdown(explicador.generar_plan_mitigacion(resultado))
    
    # Informe Completo
    with st.expander("📄 Descargar Informe Completo"):
        informe = explicador.generar_informe_completo(resultado, datos)
        st.download_button(
            label="⬇️ Descargar Informe (Markdown)",
            data=informe,
            file_name=f"informe_riesgo_{datos['nombre'].replace(' ', '_')}_{datos['fecha_evaluacion'][:10]}.md",
            mime="text/markdown"
        )


def main():
    """Función principal de la aplicación"""
    mostrar_header()
    
    # Formulario en sidebar
    datos_proveedor = formulario_proveedor()
    
    # Botón de evaluación
    if st.sidebar.button("🚀 Evaluar Proveedor", type="primary", use_container_width=True):
        # Ejecutar evaluación
        resultado = ejecutar_evaluacion(datos_proveedor)
        
        # Guardar en sesión
        st.session_state['ultimo_resultado'] = resultado
        st.session_state['ultimos_datos'] = datos_proveedor
        
        # Mostrar resultados
        mostrar_resultados(resultado, datos_proveedor)
    
    # Si hay resultados previos, mostrarlos
    elif 'ultimo_resultado' in st.session_state:
        mostrar_resultados(
            st.session_state['ultimo_resultado'],
            st.session_state['ultimos_datos']
        )
    else:
        # Página de inicio
        st.info("👈 Complete el formulario en la barra lateral y presione **'Evaluar Proveedor'** para comenzar.")
        
        st.markdown("""
        ### 🎯 Características del Sistema
        
        Este sistema experto evalúa proveedores en **4 dimensiones clave**:
        
        1. **💰 Riesgo Financiero**
           - Liquidez corriente
           - Nivel de endeudamiento
           - Rentabilidad
           - Historial de pagos
        
        2. **⚙️ Riesgo Operacional**
           - Certificaciones de calidad
           - Capacidad de producción
           - Tasa de defectos
           - Cumplimiento de entregas
        
        3. **⚖️ Riesgo Legal**
           - Cumplimiento normativo
           - Certificaciones ambientales
           - Seguros vigentes
        
        4. **⭐ Riesgo Reputacional**
           - Calificación de mercado
           - Quejas de clientes
           - Referencias positivas
        
        ### 🔬 Metodología
        
        El sistema utiliza **encadenamiento hacia adelante** con reglas expertas que:
        - Evalúan cada indicador según umbrales establecidos
        - Identifican factores de riesgo críticos
        - Calculan una puntuación ponderada
        - Generan recomendaciones accionables
        - Proporcionan trazabilidad completa de la decisión
        
        ### ✅ Ventajas
        
        - **Transparencia total**: Cada decisión es explicable
        - **Consistencia**: Mismos criterios para todos los proveedores
        - **Rapidez**: Evaluación en segundos
        - **Trazabilidad**: Auditable y documentable
        """)


if __name__ == "__main__":
    main()