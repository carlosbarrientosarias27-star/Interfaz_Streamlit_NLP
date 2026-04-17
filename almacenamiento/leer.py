import json
import os

# Definimos las rutas base de forma relativa al proyecto
BASE_DIR = "resultados"
JSON_DIR = os.path.join(BASE_DIR, "json")
TXT_DIR = os.path.join(BASE_DIR, "txt")

def listar_analisis(extension=".json"):
    """
    Lista todos los archivos guardados en la carpeta correspondiente.
    """
    ruta = JSON_DIR if extension == ".json" else TXT_DIR
    if not os.path.exists(ruta):
        return []
    
    # Retornamos la lista de archivos ordenados (más recientes primero)
    archivos = [f for f in os.listdir(ruta) if f.endswith(extension)]
    return sorted(archivos, reverse=True)

def cargar_json(nombre_archivo):
    """
    Lee un análisis en formato JSON y lo devuelve como diccionario.
    """
    ruta = os.path.join(JSON_DIR, nombre_archivo)
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Archivo no encontrado"}
    except Exception as e:
        return {"error": f"Error al leer JSON: {str(e)}"}

def leer_txt(nombre_archivo):
    """
    Lee un análisis en formato TXT.
    """
    ruta = os.path.join(TXT_DIR, nombre_archivo)
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer reporte: {str(e)}"

def buscar_por_fecha(fecha_str):
    """
    Filtra archivos por fecha. 
    Ejemplo de entrada: '20260417'
    """
    todos = listar_analisis(".json")
    return [f for f in todos if fecha_str in f]