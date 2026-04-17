import streamlit as st
from src.analizador import AnalizadorNLP
from src.cliente import check_connection
from almacenamiento.guardar import guardar_json, guardar_txt

def render_sidebar():
    """Configura la barra lateral con estados de conexión y modelos."""
    st.sidebar.header("⚙️ Configuración")
    
    # Verificación de salud del servicio (Ollama)
    if check_connection():
        st.sidebar.success("Servidor Ollama: Conectado")
    else:
        st.sidebar.error("Servidor Ollama: Desconectado")
        st.sidebar.warning("Asegúrate de que Ollama esté corriendo localmente.")

    modelo = st.sidebar.selectbox(
        "Selecciona el modelo:",
        ["qwen2.5:0.5b", "llama3", "mistral"],
        index=0
    )
    
    st.sidebar.divider()
    st.sidebar.info("Este prototipo utiliza procesamiento local para garantizar la privacidad de los datos.")
    
    return modelo

def display_results(resultados):
    """Renderiza los resultados del análisis en componentes visuales de Streamlit."""
    st.divider()
    st.subheader("📊 Resultados del Análisis")
    
    # Layout de columnas para métricas rápidas
    col1, col2, col3 = st.columns(3)
    sent = resultados.get('sentimiento', {})
    
    with col1:
        st.metric("Sentimiento", sent.get('sentimiento', 'N/A').capitalize())
    with col2:
        st.metric("Puntuación", f"{sent.get('puntuacion', 0):.2f}")
    with col3:
        st.metric("Confianza", f"{sent.get('confianza', 0)*100:.0f}%")

    # Pestañas para organizar la información densa
    tab1, tab2, tab3 = st.tabs(["📝 Resumen e Intención", "🔍 Entidades (NER)", "📦 Datos Crudos"])
    
    with tab1:
        st.markdown(f"**Resumen Ejecutivo:** {resultados.get('resumen')}")
        intencion = resultados.get('intencion', {})
        st.write(f"**Intención Detectada:** {intencion.get('intencion_principal')} (Urgencia: {intencion.get('urgencia')})")
        st.write(f"**Acción Sugerida:** {intencion.get('accion_sugerida')}")

    with tab2:
        entidades = resultados.get('entidades', {})
        for cat, valores in entidades.items():
            if valores:
                st.write(f"**{cat.capitalize()}:** {', '.join(map(str, valores))}")

    with tab3:
        st.json(resultados)

def main_ui():
    """Función principal de la interfaz Streamlit."""
    st.set_page_config(page_title="Analizador NLP Profesional", page_icon="🚀")
    
    st.title("🚀 Analizador NLP con Ollama")
    st.markdown("Transforma texto sin estructura en datos accionables.")

    modelo_seleccionado = render_sidebar()

    # Área de entrada de texto
    texto_input = st.text_area(
        "Introduce el texto a analizar:",
        placeholder="Ej: Llevo tres días intentando contactar con soporte...",
        height=200
    )

    if st.button("Ejecutar Análisis", type="primary"):
        if not texto_input:
            st.warning("Por favor, ingresa un texto para comenzar.")
            return

        # Instanciamos el analizador modularizado
        analizador = AnalizadorNLP(modelo=modelo_seleccionado)
        
        with st.spinner(f"Analizando con {modelo_seleccionado}..."):
            try:
                # Ejecutamos la lógica que antes estaba en demostrar_capacidades_nlp()
                resultados = analizador.procesar_texto_completo(texto_input)
                
                # Mostramos resultados
                display_results(resultados)
                
                # Persistencia automática (SRP)
                guardar_json(resultados)
                guardar_txt(resultados)
                st.toast("Resultados guardados en la carpeta resultados/")
                
            except Exception as e:
                st.error(f"Error en el procesamiento: {e}")

if __name__ == "__main__":
    main_ui()