import ollama
import json
from src.cliente import get_client
from src.niveles import analizar_sentimiento, extraer_entidades, detectar_intencion, generar_resumen

class AnalizadorNLP:
    def __init__(self, modelo="qwen2.5:0.5b"):
        self.modelo = modelo
        # En una implementación real, get_client() podría devolver la instancia
        self.client = get_client()

    def procesar_texto_completo(self, texto: str):
     """Ejecuta los 5 niveles de análisis y asegura la estabilidad de la UI"""
    try:
        resultados = {
            "sentimiento": analizar_sentimiento(self.client, texto, self.modelo),
            "entidades": extraer_entidades(self.client, texto, self.modelo),
            "intencion": detectar_intencion(self.client, texto, self.modelo),
            "resumen": generar_resumen(self.client, texto, self.modelo),
            # QUINTO ANÁLISIS OBLIGATORIO:
            "clasificacion": clasificar_ticket(self.client, texto, self.modelo) 
        }
        
        # Lógica de guardado automático (Requisito Bloque 7)
        self.guardar_resultado(resultados)
        
        return resultados

    except Exception as e:
        # En lugar de romper la app, devolvemos una estructura vacía coherente
        print(f"Log de error: {e}") # Para depuración en consola
        return {
            "sentimiento": {"etiqueta": "Error", "confianza": 0.0},
            "entidades": [],
            "intencion": {"tipo": "Error", "accion": "Reintentar análisis"},
            "resumen": {"breve": "No disponible", "medio": str(e), "detallado": "Error de conexión"},
            "clasificacion": {"tema": "N/A", "prioridad": "Baja"}
        }

    def validar_respuesta_json(self, response_content):
        """Asegura que la respuesta de Ollama sea un JSON válido"""
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            return {"error": "No se pudo parsear el JSON", "raw": response_content}