import ollama
import json
from src.cliente import get_client
from src.niveles import analizar_sentimiento, extraer_entidades, detectar_intencion, generar_resumen

class AnalizadorNLP:
    def __init__(self, modelo="qwen2.5:0.5b"):
        self.modelo = modelo
        # En una implementación real, get_client() podría devolver la instancia
        self.client = ollama 

    def procesar_texto_completo(self, texto: str):
        """Ejecuta todos los niveles de análisis sobre un texto"""
        try:
            resultados = {
                "sentimiento": analizar_sentimiento(self.client, texto, self.modelo),
                "entidades": extraer_entidades(self.client, texto, self.modelo),
                "intencion": detectar_intencion(self.client, texto, self.modelo),
                "resumen": generar_resumen(self.client, texto, self.modelo)
            }
            return resultados
        except Exception as e:
            raise Exception(f"Error crítico en el flujo de análisis: {e}")

    def validar_respuesta_json(self, response_content):
        """Asegura que la respuesta de Ollama sea un JSON válido"""
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            return {"error": "No se pudo parsear el JSON", "raw": response_content}