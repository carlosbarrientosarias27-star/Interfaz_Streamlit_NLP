import os, json, datetime
from src.niveles import *

class AnalizadorNLP:
    def __init__(self, modelo="qwen2.5:0.5b"):
        from src.cliente import get_client
        self.modelo = modelo
        self.client = get_client()

    def procesar_texto_completo(self, texto: str):
        try:
            resultados = {
                "sentimiento": analizar_sentimiento(self.client, texto, self.modelo),
                "entidades": extraer_entidades(self.client, texto, self.modelo),
                "intencion": detectar_intencion(self.client, texto, self.modelo),
                "resumen": generar_resumen(self.client, texto, self.modelo),
                "clasificacion": clasificar_ticket(self.client, texto, self.modelo)
            }
            # Guardado automático
            self.guardar_en_log(resultados)
            return resultados
        except Exception as e:
            # Captura amigable para no romper Streamlit
            return {"error": str(e)}

    def guardar_en_log(self, datos):
        if not os.path.exists('logs'): os.makedirs('logs')
        path = f"logs/analisis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        return path