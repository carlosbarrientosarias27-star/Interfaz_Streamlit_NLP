import os 
import sys 
import streamlit as st
import datetime
import json

# Configuración de rutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analizador import AnalizadorNLP
from src.cliente import check_connection

def setup_styles():
    st.set_page_config(page_title="Tickets Soporte NLP", page_icon="🎫", layout="wide")
    st.markdown("""
        <style>
        .stBadge { font-size: 1.2rem !important; }
        .terminal-box { background-color: #0e1117; color: #00ff00; padding: 15px; border-radius: 5px; font-family: monospace; }
        .priority-high { color: #ff4b4b; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

def main_ui():
    setup_styles()
    # Inicialización del analizador
    analizador = AnalizadorNLP(modelo="qwen2.5:7b")

    # --- SIDEBAR (Ejemplos Disponibles) ---
    with st.sidebar:
        st.header("📋 Información")
        st.markdown("""
        **Capacidades:**
        * 🔵 Análisis de Sentimiento
        * 🟢 Extracción de Entidades (NER)
        * 🟡 Detección de Intención
        * 🟠 Resumen (3 niveles)
        * 🔴 Clasificación Multicategoría
        """)
        st.divider()
        st.markdown("### 📂 Ejemplos Disponibles")
        ejemplos = {
            "Problema de Acceso": "No puedo entrar a mi cuenta corporativa. Me da error de password.",
            "Error de Facturación": "Tengo un cargo duplicado en mi tarjeta de crédito de 50€.",
            "Consulta Técnica": "¿Cómo exporto los logs en formato JSON desde la consola de administración?"
        }
        for nombre, texto_ej in ejemplos.items():
            if st.button(f"📄 {nombre}"):
                st.session_state.input_text = texto_ej

    # --- HEADER ---
    st.markdown("<h2 style='text-align: center;'>🗃️ Sistema de Análisis de Tickets de Soporte con NLP</h2>", unsafe_allow_html=True)
    
    c_status, c_model = st.columns([4, 1])
    with c_status:
        if check_connection():
            st.success("Ollama conectado", icon="✅")
    with c_model:
        st.info(f"🤖 {analizador.modelo}")

    col_izq, col_der = st.columns([1, 1.2])

    with col_izq:
        st.markdown("### 📄 Texto de entrada")
        texto_input = st.text_area("ticket", value=st.session_state.get('input_text', ""), height=250, label_visibility="collapsed")
        
        btn_analizar = st.button("🚀 ANALIZAR TICKET", use_container_width=True, type="primary")
        
        if st.button("🗑 Limpiar"):
            st.session_state.input_text = ""
            st.rerun()

    with col_der:
        # ESTE ES EL BLOQUE QUE DEBES INSERTAR
        if btn_analizar and texto_input:
            with st.spinner("Analizando..."):
                # Se ejecutan los 5 niveles y el guardado automático
                res = analizador.procesar_texto_completo(texto_input)
                
            if res:
                # 1. RENDERIZADO DE TABS (Aquí insertas tus pestañas actuales)
                t = st.tabs(["😊 Sentimiento", "🔍 Entidades", "🎯 Intención", "📝 Resumen", "📊 Clasificación"])
                
                with t[0]: # Sentimiento
                    s = res.get('sentimiento', {})
                    st.metric("Etiqueta", s.get('etiqueta', 'N/A'))
                    st.progress(s.get('confianza', 0.0))

                # ... (resto de tus pestañas t[1], t[2], t[3], t[4]) ...

                # 2. CONFIRMACIÓN DE GUARDADO (Requisito Bloque 7)
                # 'ruta_archivo' debe venir del retorno de procesar_texto_completo
                ruta = res.get('ruta_archivo', 'logs/analisis_reciente.json')
                st.success(f"✅ Análisis completado y guardado automáticamente en: `{ruta}`")
            
            else:
                st.error("❌ Error crítico en el análisis. Revisa la conexión con Ollama.")
        
        else:
            # Estado inicial antes de pulsar el botón
            st.info("Introduce un ticket y pulsa 'Analizar' para ver los resultados.")

if __name__ == "__main__":
    main_ui()