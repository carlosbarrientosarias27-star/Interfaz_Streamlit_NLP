# ============================================
# DEMOSTRACIÓN DE CAPACIDADES NLP CON OLLAMA
# ============================================
import os
import json
import ollama  # Importamos la librería oficial de ollama

def demostrar_capacidades_nlp(texto: str):
    """Demuestra múltiples capacidades NLP sobre un mismo texto usando Ollama"""
    
    # Configuramos el modelo a usar (puedes usar 'llama3', 'qwen2.5:0.5b', 'qwen2.5:0.8b', etc.)
    MODELO = "qwen2.5:0.5b"
    
    print("=" * 70)
    print(f"📝 TEXTO ORIGINAL: {texto}")
    print("=" * 70)
    
    # 1. ANÁLISIS DE SENTIMIENTO
    print("\n🔵 1. ANÁLISIS DE SENTIMIENTO")
    print("-" * 50)
    
    response_sentimiento = ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": """
            Analiza el sentimiento del texto. Responde ÚNICAMENTE en formato JSON con:
            - sentimiento: positivo, negativo o neutral
            - puntuacion: número del 0 al 1 (0=muy negativo, 1=muy positivo)
            - emociones: lista de emociones detectadas
            - confianza: número del 0 al 1
            """},
            {"role": "user", "content": texto}
        ],
        format="json" # Ollama fuerza la salida a JSON válido
    )
    
    try:
        sentimiento = json.loads(response_sentimiento['message']['content'])
        print(f"   Sentimiento: {sentimiento.get('sentimiento')}")
        print(f"   Puntuación: {sentimiento.get('puntuacion')}")
        print(f"   Emociones: {sentimiento.get('emociones')}")
    except Exception as e:
        print(f"   Error al parsear: {e}")
    
    # 2. EXTRACCIÓN DE ENTIDADES (NER)
    print("\n🔵 2. EXTRACCIÓN DE ENTIDADES (NER)")
    print("-" * 50)
    
    response_ner = ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": """
            Extrae las entidades. Responde ÚNICAMENTE en JSON con:
            personas, organizaciones, lugares, fechas, cantidades, otros.
            """},
            {"role": "user", "content": texto}
        ],
        format="json"
    )
    
    try:
        entidades = json.loads(response_ner['message']['content'])
        for categoria, valores in entidades.items():
            if valores:
                print(f"   {categoria.capitalize()}: {valores}")
    except:
        print("   No se pudieron extraer entidades.")

    # 3. DETECCIÓN DE INTENCIÓN
    print("\n🔵 3. DETECCIÓN DE INTENCIÓN")
    print("-" * 50)
    
    response_intencion = ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": "Detecta la intención. Responde en JSON con: intencion_principal, subcategoria, urgencia, accion_sugerida."},
            {"role": "user", "content": texto}
        ],
        format="json"
    )
    
    try:
        intencion = json.loads(response_intencion['message']['content'])
        print(f"   Intención: {intencion.get('intencion_principal')} ({intencion.get('urgencia')})")
        print(f"   Acción: {intencion.get('accion_sugerida')}")
    except:
        print("   Error en detección de intención.")

    # 4. RESUMEN (Simplificado para Ollama)
    print("\n🔵 4. RESUMEN")
    print("-" * 50)
    
    response_resumen = ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": "Resume el texto en una sola frase potente."},
            {"role": "user", "content": texto}
        ]
    )
    print(f"   Resumen: {response_resumen['message']['content'].strip()}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    texto_queja = """
    Llevo tres días intentando contactar con soporte y nadie responde. 
    Mi pedido #12345 debería haber llegado el martes y aún no ha llegado. 
    Estoy muy molesto porque necesito el producto para un proyecto urgente. 
    Si no me solucionan hoy, cancelo el pedido y pido devolución.
    """
    
    try:
        demostrar_capacidades_nlp(texto_queja)
    except Exception as e:
        print(f"❌ Error: ¿Está Ollama corriendo? {e}")