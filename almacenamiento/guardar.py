import json
import os
from datetime import datetime

# Configuración de rutas relativas
BASE_DIR = "resultados"
JSON_DIR = os.path.join(BASE_DIR, "json")
TXT_DIR = os.path.join(BASE_DIR, "txt")

def _verificar_directorios():
    """Asegura que las carpetas de destino existan antes de guardar."""
    for directorio in [JSON_DIR, TXT_DIR]:
        if not os.path.exists(directorio):
            os.makedirs(directorio)

def guardar_json(data: dict):
    """
    Guarda los resultados del análisis NLP en un archivo .json con timestamp.
    """
    _verificar_directorios()
    
    # Generar nombre único: analisis_20260417_130000.json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"analisis_{timestamp}.json"
    ruta_completa = os.path.join(JSON_DIR, nombre_archivo)
    
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return ruta_completa
    except Exception as e:
        print(f"Error al guardar JSON: {e}")
        return None

def guardar_txt(data: dict):
    """
    Transforma el diccionario de resultados en un reporte legible .txt.
    """
    _verificar_directorios()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"reporte_{timestamp}.txt"
    ruta_completa = os.path.join(TXT_DIR, nombre_archivo)
    
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write(f"REPORTE DE ANÁLISIS NLP - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"📝 RESUMEN:\n{data.get('resumen', 'Sin resumen')}\n\n")
            
            sent = data.get('sentimiento', {})
            f.write(f"📊 SENTIMIENTO: {sent.get('sentimiento', 'N/A').upper()}\n")
            f.write(f"   Confianza: {sent.get('confianza', 0) * 100}%\n\n")
            
            entidades = data.get('entidades', {})
            f.write("🔍 ENTIDADES DETECTADAS:\n")
            for cat, vals in entidades.items():
                if vals:
                    f.write(f"   - {cat.capitalize()}: {', '.join(map(str, vals))}\n")
                    
        return ruta_completa
    except Exception as e:
        print(f"Error al generar reporte TXT: {e}")
        return None