"""
Componentes reutilizables para la interfaz de usuario
"""
import plotly.graph_objects as go


def crear_gauge_puntuacion(puntuacion: float):
    """
    Crea un gráfico de tipo gauge para mostrar la puntuación de riesgo
    
    Args:
        puntuacion: Valor de la puntuación (0-100)
        
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
            ]
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def crear_banner():
    """Crea el banner principal de la aplicación"""
    return '<div class="banner"><h1>Sistema Experto de Evaluación de Riesgo de Proveedores</h1></div>'


def crear_tarjeta_categoria(icono: str, titulo: str, texto: str):
    """
    Crea una tarjeta de categoría para la página de inicio
    
    Args:
        icono: Emoji o icono a mostrar
        titulo: Título de la categoría
        texto: Descripción de la categoría
        
    Returns:
        HTML de la tarjeta
    """
    return f"""
    <div class='category-card'>
        <div class='category-icon'>{icono}</div>
        <div class='category-title'>{titulo}</div>
        <div class='category-text'>{texto}</div>
    </div>
    """


def crear_tarjeta_resultado(titulo: str, valor: str, color: str = "#000"):
    """
    Crea una tarjeta de resultado
    
    Args:
        titulo: Título de la métrica
        valor: Valor a mostrar
        color: Color del valor (opcional)
        
    Returns:
        HTML de la tarjeta
    """
    return f"""
    <div class='result-card'>
        <div class='result-title'>{titulo}</div>
        <div class='result-value' style='color:{color};'>{valor}</div>
    </div>
    """


def crear_caja_regla(regla: str, razonamiento: str, impacto: str):
    """
    Crea una caja de regla activada
    
    Args:
        regla: Nombre de la regla
        razonamiento: Explicación del razonamiento
        impacto: Impacto de la regla
        
    Returns:
        HTML de la caja de regla
    """
    return f"""
    <div class='rule-box'>
        <b>{regla}</b><br>
        <i>{razonamiento}</i><br>
        <span style='color:#555;'>Impacto: {impacto}</span>
    </div>
    """


def crear_disclaimer():
    """Crea el mensaje de disclaimer"""
    return """
    <div class='disclaimer'>
        ⚠️ <b>Descargo de responsabilidad en base al análisis de resultados:</b><br>
        Este sistema experto realiza una evaluación automatizada basada en reglas predefinidas y datos ingresados por el usuario.
        Los resultados, puntuaciones y recomendaciones deben interpretarse como un apoyo a la toma de decisiones,
        no como un dictamen financiero o legal definitivo. Se recomienda validar los resultados con un análisis profesional adicional.
    </div>
    """


def crear_footer():
    """Crea el footer con información del equipo"""
    return """
    <div style='text-align:center; margin-top:30px'>
        <h4>👩‍💻 Desarrollado por el <b>Grupo N°2 - Escuela de Ingeniería de Sistemas</b></h4>
        <p>
        Chávez Alva Tania Ycela -- Cruz Esquivel Luis Josmell -- Cruz Vargas Germain Alexander -- Rodríguez Sandoval Harry Sly -- Villa Valdiviezo Favián Enrique
        </p>
    </div>
    """