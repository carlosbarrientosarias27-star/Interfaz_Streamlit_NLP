import ollama

def get_client():
    """
    Retorna la instancia del cliente de Ollama.
    En la librería oficial, el cliente es el propio módulo, 
    pero centralizarlo aquí permite añadir configuraciones futuras
    como HOST, PORT o timeouts personalizados.
    """
    return ollama

def check_connection():
    """
    Verifica si el servicio de Ollama está respondiendo.
    Útil para mostrar alertas en la interfaz de Streamlit.
    """
    try:
        # Intentamos listar los modelos como heartbeat
        ollama.list()
        return True
    except Exception:
        return False

def check_model_availability(model_name: str):
    """
    Comprueba si el modelo específico (ej. 'qwen2.5:0.5b') está descargado.
    """
    try:
        models = ollama.list()
        # Verificamos si el nombre del modelo existe en la lista local
        return any(m['name'] == model_name for m in models.get('models', []))
    except Exception:
        return False