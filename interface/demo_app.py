import os 
import sys 
import streamlit as st
import datetime

# Configuración de rutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analizador import AnalizadorNLP
from src.cliente import check_connection

def setup_styles():
    st.set_page_config(page_title="Tickets Soporte NLP", page_icon="🎫", layout="wide")
    
    st.markdown("""
        <style>
        /* Fondo gris muy oscuro para los contenedores */
        [data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
            background-color: #262730; /* Gris oscuro corporativo */
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #41444c;
        }

        /* Botones con esquinas redondeadas y colores vibrantes */
        div.stButton > button {
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 20px;
            transition: 0.3s;
        }

        /* Colores exactos de la Imagen 2 */
        .btn-azul button { background-color: #3498db !important; }    /* Cargar */
        .btn-rojo button { background-color: #e74c3c !important; }    /* Limpiar */
        .btn-verde button { background-color: #2ecc71 !important; }   /* Cargar JSON */
        .btn-naranja button { background-color: #f39c12 !important; } /* Procesar */

        /* La terminal de la derecha */
        .terminal-box {
            background-color: #121212;
            border: 1px solid #333;
            color: #2ecc71; /* Verde neón */
            font-family: 'Consolas', monospace;
            padding: 15px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def main_ui():
    setup_styles()
    analizador = AnalizadorNLP(modelo="qwen2.5:7b")

    # --- SIDEBAR (Ejemplos Disponibles) ---
    with st.sidebar:
        st.markdown("### 📂 Ejemplos Disponibles")
        ejemplos = {
            "Problema de Acceso": "No puedo entrar a mi cuenta corporativa...",
            "Error de Facturación": "Tengo un cargo duplicado en mi tarjeta...",
            "Consulta Técnica": "¿Cómo exporto los logs en formato JSON?"
        }
        for nombre, texto_ej in ejemplos.items():
            if st.button(f"📄 {nombre}"):
                st.session_state.input_text = texto_ej

    # --- HEADER ---
    st.markdown("<h2 style='text-align: center;'>🗃️ Sistema de Análisis de Tickets de Soporte con NLP</h2>", unsafe_allow_html=True)
    
    c_status, c_model = st.columns([4, 1])
    with c_status:
        if check_connection():
            st.markdown('<span style="color: #39d353; border: 1px solid #39d353; padding: 2px 8px; border-radius: 4px;">☑ Ollama conectado</span>', unsafe_allow_html=True)
    with c_model:
        st.markdown(f'<p style="text-align: right; color: #8b949e;">🤖 Modelo: {analizador.modelo}</p>', unsafe_allow_html=True)

    col_izq, col_der = st.columns([1, 1.2])

    with col_izq:
        # Bloque de Entrada
        with st.container():
            st.markdown("### 📄 Ticket a analizar")
            texto_input = st.text_area("ticket", value=st.session_state.get('input_text', ""), height=200, label_visibility="collapsed")
            
            b1, b2 = st.columns(2)
            with b1:
                st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
                if st.button("📥 Cargar ejemplo"): pass
                st.markdown('</div>', unsafe_allow_html=True)
            with b2:
                st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
                if st.button("🗑 Limpiar"):
                    st.session_state.input_text = ""
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # Bloque de Lotes
        with st.container():
            st.markdown("### 👥 Procesamiento por lotes")
        
            # Botón Cargar JSON (Verde)
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            st.button("📂 Cargar JSON con tickets")
            st.markdown('</div>', unsafe_allow_html=True)

            # Botón Procesar Lote (Naranja)    
            st.markdown('<div class="btn-naranja">', unsafe_allow_html=True)
            ejecutar = st.button("⚡ Procesar lote")
            st.markdown('</div>', unsafe_allow_html=True)

            # BANNER DE ESTADO (Verde brillante solicitado)
            st.markdown('<div class="banner-procesando">⌛ PROCESANDO LOTE...</div>', unsafe_allow_html=True)
            st.progress(0.4)
            st.caption("📄 Procesando ticket 1/1...")

    with col_der:
        t = st.tabs(["🔄 Pipeline", "⚡ Acciones", "📄 JSON", "📊 Modelos"])
        with t[0]:
            if ejecutar and texto_input:
                res = analizador.procesar_texto_completo(texto_input)
                st.markdown(f"""
                <div class="terminal-box">
                ================================================================================<br>
                🟢 PROCESANDO LOTE DE 1 TICKETS<br>
                ================================================================================<br>
                | Analizando sentimiento: {res['sentimiento']['etiqueta'] if 'sentimiento' in res else 'OK'}<br>
                | Extrayendo entidades...<br>
                | Generando resumen...<br>
                <br>
                ✅ Análisis completado y guardado automáticamente
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="terminal-box">
                Esperando entrada para analizar...
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main_ui()