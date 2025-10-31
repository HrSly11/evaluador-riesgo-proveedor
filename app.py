from engine import MotorEvaluacionRiesgo, DatosProveedor, ExplicadorDecisiones
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go

# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(
    page_title="Evaluador de Riesgo de Proveedores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== ESTILOS CSS PERSONALIZADOS ==========
st.markdown("""
<style>
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

    /* === Cuadros de resultados uniformes === */
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

    /* === Tarjetas de categorías (inicio) === */
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

    /* === Reglas activadas === */
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
    
    /* === Espaciado del bloque de instrucciones === */
    .stMarkdown > div:has(.instructions-block) {
        margin-top: 2.5rem !important;
    }
    
    /* === Espaciado para botones y elementos === */
    .stDownloadButton {
        margin-top: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }

</style>
""", unsafe_allow_html=True)


# ========== FUNCIONES AUXILIARES ==========
def crear_gauge_puntuacion(puntuacion: float):
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
            ]
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig


# ========== FORMULARIO DE PROVEEDOR ==========
def formulario_proveedor():
    st.sidebar.header("📝 Datos del Proveedor")

    # ====== Sección General ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("📌 Información General")
    datos = {}
    datos['nombre'] = st.sidebar.text_input("Nombre del Proveedor", "Proveedor XYZ S.A.")
    datos['industria'] = st.sidebar.selectbox(
        "Industria",
        [
            "Manufactura", "Servicios", "Tecnología", "Construcción", "Logística",
            "Agricultura", "Minería", "Salud", "Educación", "Retail", "Energía",
            "Transporte", "Finanzas", "Turismo", "Textil"
        ],
        help="Selecciona el sector al que pertenece el proveedor."
    )
    datos['tiempo_mercado'] = st.sidebar.number_input("Años en el mercado", 0.0, 100.0, 5.0, 0.5)

    # ====== Sección Financiera ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Indicadores Financieros")
    datos['liquidez_corriente'] = st.sidebar.slider("Ratio de Liquidez Corriente", 0.0, 5.0, 1.5, 0.1)
    datos['endeudamiento'] = st.sidebar.slider("Nivel de Endeudamiento", 0.0, 1.0, 0.5, 0.05)
    datos['rentabilidad'] = st.sidebar.slider("Rentabilidad (%)", -50.0, 50.0, 10.0, 1.0) / 100
    datos['historial_pagos'] = st.sidebar.slider("Pagos Puntuales (%)", 0.0, 100.0, 85.0, 5.0)

    # ====== Sección Operacional ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Indicadores Operacionales")
    datos['certificacion_calidad'] = st.sidebar.checkbox("Certificación de Calidad (ISO 9001)", True)
    datos['capacidad_produccion'] = st.sidebar.slider("Capacidad de Producción (%)", 0.0, 100.0, 75.0, 5.0)
    datos['tasa_defectos'] = st.sidebar.slider("Tasa de Defectos (%)", 0.0, 20.0, 3.0, 0.5)
    datos['cumplimiento_entregas'] = st.sidebar.slider("Cumplimiento de Entregas (%)", 0.0, 100.0, 90.0, 5.0)

    # ====== Sección Legal ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚖️ Indicadores Legales")
    datos['cumplimiento_legal'] = st.sidebar.checkbox("Cumplimiento Legal Completo", True)
    datos['certificacion_ambiental'] = st.sidebar.checkbox("Certificación Ambiental (ISO 14001)", False)
    datos['seguros_vigentes'] = st.sidebar.checkbox("Seguros de Responsabilidad Vigentes", True)

    # ====== Sección Reputacional ======
    st.sidebar.markdown("---")
    st.sidebar.subheader("⭐ Indicadores Reputacionales")
    datos['calificacion_mercado'] = st.sidebar.slider("Calificación de Mercado", 1.0, 5.0, 4.0, 0.1)
    datos['quejas_clientes'] = st.sidebar.number_input("Quejas de Clientes (último año)", 0, 100, 3)
    datos['referencias_positivas'] = st.sidebar.number_input("Referencias Positivas Verificadas", 0, 20, 5)

    datos['fecha_evaluacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return datos


# ========== MOSTRAR RESULTADOS ==========
def mostrar_resultados(resultado, datos):
    explicador = ExplicadorDecisiones()
    st.markdown("## 📈 Resultados de la Evaluación")

    col1, col2, col3 = st.columns(3)
    color = {'BAJO': 'green', 'MODERADO': 'orange', 'ALTO': 'red', 'CRÍTICO': '#b71c1c'}.get(resultado['riesgo_final'], 'gray')

    with col1:
        st.markdown(f"<div class='result-card'><div class='result-title'>Nivel de Riesgo</div><div class='result-value' style='color:{color};'>{resultado['riesgo_final']}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='result-card'><div class='result-title'>Puntuación</div><div class='result-value'>{resultado['puntuacion']:.0f}/100</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='result-card'><div class='result-title'>Reglas Activadas</div><div class='result-value'>{resultado['total_reglas_activadas']}</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.plotly_chart(crear_gauge_puntuacion(resultado['puntuacion']), use_container_width=True)

    if resultado['riesgo_final'] in ['BAJO', 'MODERADO']:
        st.success(resultado['recomendacion'])
    else:
        st.warning(resultado['recomendacion'])

    if resultado.get('explicaciones'):
        st.markdown("### ⚙️ Reglas Activadas y Explicaciones")
        for exp in resultado['explicaciones']:
            st.markdown(f"""
            <div class='rule-box'>
                <b>{exp['regla']}</b><br>
                <i>{exp['razonamiento']}</i><br>
                <span style='color:#555;'>Impacto: {exp['impacto']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No se activaron reglas específicas para este proveedor.")

    informe_md = explicador.generar_informe_completo(resultado, datos)
    st.download_button(
        label="⬇️ Descargar informe...",
        data=informe_md,
        file_name=f"informe_{datos['nombre'].replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True
    )

    st.markdown("""
    <div class='disclaimer'>
        ⚠️ <b>Descargo de responsabilidad en base al análisis de resultados:</b><br>
        Este sistema experto realiza una evaluación automatizada basada en reglas predefinidas y datos ingresados por el usuario.
        Los resultados, puntuaciones y recomendaciones deben interpretarse como un apoyo a la toma de decisiones,
        no como un dictamen financiero o legal definitivo. Se recomienda validar los resultados con un análisis profesional adicional.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔁 Hacer una nueva evaluación...", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ========== MAIN APP ==========
def main():
    st.markdown('<div class="banner"><h1>Sistema Experto de Evaluación de Riesgo de Proveedores</h1></div>', unsafe_allow_html=True)

    datos = formulario_proveedor()

    if st.sidebar.button("🚀 Evaluar Proveedor", type="primary", use_container_width=True):
        motor = MotorEvaluacionRiesgo()
        motor.reset()
        motor.declare(DatosProveedor(**{k: v for k, v in datos.items() if k not in ['nombre', 'fecha_evaluacion']}))
        with st.spinner("Evaluando proveedor..."):
            motor.run()
        resultado = motor.obtener_resultado()
        st.session_state['resultado'] = resultado
        st.session_state['datos'] = datos
        mostrar_resultados(resultado, datos)

    elif 'resultado' in st.session_state:
        mostrar_resultados(st.session_state['resultado'], st.session_state['datos'])

    else:
        st.markdown("<h2 style='text-align:center;'>🏠 Bienvenido</h2>", unsafe_allow_html=True)
        st.markdown("""
        <p style='text-align:center; font-size:17px;'>
        Este sistema experto analiza proveedores en 4 dimensiones: <b>Financiera</b>, <b>Operacional</b>, <b>Legal</b> y <b>Reputacional</b>.
        Utiliza un motor de inferencia basado en reglas y proporciona trazabilidad completa de las decisiones.
        </p>
        """, unsafe_allow_html=True)

        colA, colB, colC, colD = st.columns(4)
        with colA:
            st.markdown("<div class='category-card'><div class='category-icon'>💰</div><div class='category-title'>Financiero</div><div class='category-text'>Liquidez, endeudamiento y rentabilidad</div></div>", unsafe_allow_html=True)
        with colB:
            st.markdown("<div class='category-card'><div class='category-icon'>⚙️</div><div class='category-title'>Operacional</div><div class='category-text'>Capacidad, entregas y calidad</div></div>", unsafe_allow_html=True)
        with colC:
            st.markdown("<div class='category-card'><div class='category-icon'>⚖️</div><div class='category-title'>Legal</div><div class='category-text'>Cumplimiento normativo y seguros</div></div>", unsafe_allow_html=True)
        with colD:
            st.markdown("<div class='category-card'><div class='category-icon'>🌐</div><div class='category-title'>Reputacional</div><div class='category-text'>Reputación, quejas y referencias</div></div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
        
        st.info("""
        **Instrucciones:**
        
        1️⃣ Completa los datos del proveedor en el menú lateral.
          
        2️⃣ Presiona **"🚀 Evaluar Proveedor"**.
          
        3️⃣ Visualiza el resultado y descarga el informe generado.
        """)

        st.markdown("""
        <div style='text-align:center; margin-top:30px'>
            <h4>👩‍💻 Desarrollado por el <b>Grupo N°2 - Escuela de Ingeniería de Sistemas</b></h4>
            <p>
            Chávez Alva Tania Ycela -- Cruz Esquivel Luis Josmell -- Cruz Vargas Germain Alexander -- Rodríguez Sandoval Harry Sly -- Villa Valdiviezo Favián Enrique
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()