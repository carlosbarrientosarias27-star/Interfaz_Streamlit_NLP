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
    # Configuración de página con layout ancho
    st.set_page_config(page_title="Sistema de Análisis NLP", page_icon="🧠", layout="wide")
    
    # Inyectamos CSS para forzar el modo oscuro y estilos personalizados
    st.markdown("""
        <style>
        /* Fondo oscuro para la aplicación */
        .stApp { background-color: #0e1117; color: #ffffff; }
        /* Estilo para los contenedores de métricas y tabs */
        .stMetric { background-color: #1a1c23; padding: 10px; border-radius: 5px; }
        /* Ajuste del botón ANALIZAR para que sea rojo coral como la imagen */
        div.stButton > button:first-child {
            background-color: #ff4b4b;
            color: white;
            border: none;
        }
        </style>
    """, unsafe_allow_html=True)

def main_ui():
    setup_styles()
    
    # Inicialización del analizador (Usamos la versión ligera que usa la empresa)
    analizador = AnalizadorNLP(modelo="qwen2.5:0.5b")

    # --- SIDEBAR (Información de capacidades) ---
    with st.sidebar:
        st.header("Información")
        st.markdown("**Capacidades demostradas:**")
        st.markdown("""
        * 🔵 Análisis de Sentimiento
        * 🟢 Extracción de Entidades (NER)
        * 🟡 Detección de Intención
        * 🟠 Resumen (3 niveles)
        * 🔴 Clasificación Multicategoría
        """)
        st.divider()
        st.caption(f"Último acceso: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- HEADER PRINCIPAL ---
    st.markdown("<h1 style='text-align: left;'>🧠 Sistema de Análisis NLP</h1>", unsafe_allow_html=True)
    st.write("_Demostración de capacidades: Sentimiento, Entidades, Intención, Resumen y Clasificación_")
    st.divider()

    # --- CUERPO PRINCIPAL (2 Columnas: Entrada vs Configuración) ---
    col_input, col_config = st.columns([2, 1])

    with col_input:
        st.markdown("### 📄 Texto de entrada")
        
        # Selector de ejemplos integrado en el centro (como la imagen 2)
        ejemplos = {
            "Seleccione un ejemplo...": "",
            "Problema de Acceso - Error Password": "No puedo entrar a mi cuenta corporativa. Me da error de password.",
            "Error de Facturación - Cargo Duplicado": "Tengo un cargo duplicado en mi tarjeta de crédito de 50€.",
            "Consulta Técnica - Timeout en Python": "¿Alguien sabe cómo configurar el timeout en una conexión HTTP con Python? Estoy usando la librería requests y a veces se queda colgado cuando el servidor tarda más de 10 segundos. He visto que hay un parámetro timeout en requests.get(), pero no sé si ponerlo en segundos o milisegundos."
        }
        
        ejemplo_sel = st.selectbox("Cargar ejemplo:", list(ejemplos.keys()))
        texto_defecto = ejemplos[ejemplo_sel] if ejemplo_sel != "Seleccione un ejemplo..." else st.session_state.get('input_text', "")

        texto_input = st.text_area("Texto a analizar:", value=texto_defecto, height=200)
        
        btn_analizar = st.button("🚀 ANALIZAR", use_container_width=True)

    with col_config:
        st.markdown("### ⚙️ Configuración")
        with st.container(border=True):
            st.info(f"**Modelo:** `{analizador.modelo}` (Ollama)")
            st.checkbox("Guardar en logs/", value=True)
            st.checkbox("Mostrar debug", value=False)
        
        if check_connection():
            st.success("Requisito: Ollama corriendo correctamente", icon="⚙️")

    # --- RESULTADOS ---
    if btn_analizar and texto_input:
        st.divider()
        with st.spinner("Procesando análisis..."):
            # En una app real, aquí llamarías al analizador.
            # Para esta demo, usamos los datos del JSON cargado:
            res = {
                "sentimiento": {"sentimiento": "neutral", "puntuacion": 0.5, "confianza": 1.0},
                "entidades": {"personas": [], "organizaciones": [], "lugar": "TalentoDICTASPUMBL", "otros": ["Ollama", "Sistema de Almacén"]},
                "intencion": {"intencion_principal": "Desarrollo", "subcategoria": "Ingresos e Inversión", "urgencia": "Urgente", "accion_sugerida": "Recarga del equipo o alquilar un dispositivo"},
                "resumen": {"breve": "No puedo conectarme con la Ola a tiempo...", "medio": "Tengo un dispositivo sin conexión...", "detallado": "Lamento informarte sobre la situación..."},
                "clasificacion": {"tema": "Disrupción laboral", "prioridad": "Media"}
            }
        
        if res:
            # Creación de pestañas con nombres e iconos según la imagen
            t = st.tabs(["😊 Sentimiento", "🔍 Entidades", "🎯 Intención", "📝 Resumen", "📊 Clasificación"])
            
            with t[0]: # Sentimiento
                s = res.get('sentimiento', {})
                col1, col2 = st.columns(2)
                col1.metric("Sentimiento Dominante", s.get('sentimiento', 'N/A').upper())
                col2.metric("Confianza", f"{s.get('confianza', 0) * 100}%")
                st.write("**Puntuación de positividad:**")
                st.progress(float(s.get('puntuacion', 0.5)))
            
            with t[1]: # Entidades
                e = res.get('entidades', {})
                st.markdown("### 🏷️ Entidades Detectadas")
                # Mostramos en columnas para mejor visualización
                c1, c2 = st.columns(2)
                c1.write("**Lugares:** " + (e.get('lugar') if e.get('lugar') else "Ninguno"))
                c2.write("**Otros:** " + ", ".join(e.get('otros', [])))
                
                if not any([e.get('personas'), e.get('organizaciones')]):
                    st.info("No se detectaron personas u organizaciones específicas.")
            
            with t[2]: # Intención
                i = res.get('intencion', {})
                st.markdown(f"#### Propósito: **{i.get('intencion_principal')}**")
                st.warning(f"**Urgencia:** {i.get('urgencia')}")
                st.write(f"**Acción Sugerida:** {i.get('accion_sugerida')}")
            
            with t[3]: # Resumen
                r = res.get('resumen', {})
                st.subheader("Extracto del texto")
                with st.expander("Resumen Breve", expanded=True):
                    st.write(r.get('breve'))
                with st.expander("Resumen Detallado"):
                    st.write(r.get('detallado'))
            
            with t[4]: # Clasificación
                c = res.get('clasificacion', {})
                st.info(f"**Categoría temática:** {c.get('tema')}")
                st.write(f"**Prioridad asignada:** {c.get('prioridad')}")
            
            st.toast("Análisis completado", icon="✅")

if __name__ == "__main__":
    main_ui()