import ollama
import json
import os
import datetime
from src.cliente import get_client
from src.niveles import (
    analizar_sentimiento, 
    extraer_entidades, 
    detectar_intencion, 
    generar_resumen,
    clasificar_ticket # Asegúrate de que esta función exista en niveles.py
)

class AnalizadorNLP:
    def __init__(self, modelo="qwen2.5:0.5b"):
        self.modelo = modelo
        self.client = get_client()

    def procesar_texto_completo(self, texto: str):
        """Ejecuta los 5 niveles de análisis y guarda el resultado automáticamente"""
        try:
            # Diccionario de resultados (Se añadió la coma faltante)
            resultados = {
                "sentimiento": analizar_sentimiento(self.client, texto, self.modelo),
                "entidades": extraer_entidades(self.client, texto, self.modelo),
                "intencion": detectar_intencion(self.client, texto, self.modelo),
                "resumen": generar_resumen(self.client, texto, self.modelo), # Coma añadida
                "clasificacion": clasificar_ticket(self.client, texto, self.modelo)
            }
            
            # Requisito Bloque 7: Guardado automático
            self.guardar_en_log(resultados)
            
            return resultados
        except Exception as e:
            # Captura el error para evitar que la UI colapse por completo
            print(f"Error detectado: {e}")
            raise Exception(f"Error crítico en el flujo de análisis: {e}")

    def guardar_en_log(self, datos):
        """Guarda el análisis en formato JSON dentro de la carpeta /logs"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"logs/analisis_{timestamp}.json"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        return nombre_archivo

    def validar_respuesta_json(self, response_content):
        """Asegura que la respuesta de Ollama sea un JSON válido"""
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            return {"error": "No se pudo parsear el JSON", "raw": response_content}