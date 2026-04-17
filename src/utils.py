import re

def limpiar_json(texto_sucio: str):
    """Limpia posibles artefactos de Markdown (como ```json) de la respuesta"""
    patron = r"```json\s*(.*?)\s*```"
    match = re.search(patron, texto_sucio, re.DOTALL)
    return match.group(1) if match else texto_sucio

def formatear_fecha(fecha_str):
    # Lógica para normalizar fechas extraídas por el NER
    pass

def token_counter(texto):
    # Estimación simple de tokens (palabras * 1.3 aprox para modelos ingles/español)
    return len(texto.split()) * 1.3