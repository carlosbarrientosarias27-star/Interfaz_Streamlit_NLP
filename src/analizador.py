import ollama
from src.niveles import obtener_sentimiento, extraer_entidades

class ProcesadorNLP:
    def __init__(self, modelo="qwen2.5:0.5b"):
        self.modelo = modelo
        self.client = ollama

    def analizar_texto(self, texto):
        try:
            resultados = {
                "sentimiento": obtener_sentimiento(self.client, texto, self.modelo),
                "entidades": extraer_entidades(self.client, texto, self.modelo)
            }
            return resultados
        except Exception as e:
            raise Exception(f"Error en el procesamiento: {str(e)}")