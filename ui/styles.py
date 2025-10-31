# Estilos CSS para la aplicación de evaluación de riesgo de proveedores

def get_custom_css():
    """Retorna los estilos CSS personalizados de la aplicación"""
    return """
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
"""