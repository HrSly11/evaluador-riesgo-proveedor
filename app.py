"""
Sistema Experto de Evaluación de Riesgo de Proveedores
Aplicación principal usando Streamlit
"""
from engine import MotorEvaluacionRiesgo, DatosProveedor
import streamlit as st

# Importar componentes de la carpeta ui
from ui.styles import get_custom_css
from ui.components import crear_banner
from ui.formulario import formulario_proveedor
from ui.inicio import mostrar_inicio
from ui.resultados import mostrar_resultados


# ========== CONFIGURACIÓN DE PÁGINA ==========
st.set_page_config(
    page_title="Evaluador de Riesgo de Proveedores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== APLICAR ESTILOS CSS ==========
st.markdown(get_custom_css(), unsafe_allow_html=True)


# ========== FUNCIÓN PRINCIPAL ==========
def main():
    """Función principal de la aplicación"""
    
    # Mostrar banner
    st.markdown(crear_banner(), unsafe_allow_html=True)

    # Mostrar formulario en el sidebar
    datos = formulario_proveedor()

    # Botón de evaluación en el sidebar
    if st.sidebar.button("🚀 Evaluar Proveedor", type="primary", use_container_width=True):
        # Crear motor de evaluación
        motor = MotorEvaluacionRiesgo()
        motor.reset()
        
        # Filtrar datos para el motor (excluir nombre y fecha_evaluacion)
        datos_motor = {
            k: v for k, v in datos.items() 
            if k not in ['nombre', 'fecha_evaluacion']
        }
        
        # Declarar hechos y ejecutar motor
        motor.declare(DatosProveedor(**datos_motor))
        
        with st.spinner("Evaluando proveedor..."):
            motor.run()
        
        # Obtener y guardar resultados en session_state
        resultado = motor.obtener_resultado()
        st.session_state['resultado'] = resultado
        st.session_state['datos'] = datos
        
        # Mostrar resultados
        mostrar_resultados(resultado, datos)

    # Si ya hay resultados en session_state, mostrarlos
    elif 'resultado' in st.session_state:
        mostrar_resultados(st.session_state['resultado'], st.session_state['datos'])

    # Si no hay resultados, mostrar página de inicio
    else:
        mostrar_inicio()


if __name__ == "__main__":
    main()