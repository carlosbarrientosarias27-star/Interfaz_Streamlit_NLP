import json

def analizar_sentimiento(client, texto, modelo):
    system_prompt = """Analiza el sentimiento. Responde ÚNICAMENTE en JSON: 
    {"sentimiento": "positivo/negativo/neutral", "puntuacion": 0.0-1.0, "emociones": [], "confianza": 0.0-1.0}"""
    
    response = client.chat(
        model=modelo,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": texto}],
        format="json"
    )
    return json.loads(response['message']['content'])

def extraer_entidades(client, texto, modelo):
    system_prompt = "Extrae entidades. Responde ÚNICAMENTE en JSON con: personas, organizaciones, lugares, fechas, cantidades, otros."
    
    response = client.chat(
        model=modelo,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": texto}],
        format="json"
    )
    return json.loads(response['message']['content'])

def detectar_intencion(client, texto, modelo):
    system_prompt = "Detecta intención. Responde en JSON con: intencion_principal, subcategoria, urgencia, accion_sugerida."
    
    response = client.chat(
        model=modelo,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": texto}],
        format="json"
    )
    return json.loads(response['message']['content'])

def generar_resumen(client, texto, modelo):
    """Genera tres niveles de resumen como requiere la interfaz"""
    prompt = f"""Genera tres resúmenes del siguiente ticket en formato JSON:
    - "breve": Una frase corta.
    - "medio": Un párrafo explicativo.
    - "detallado": Análisis completo de puntos clave.
    Texto: {texto}"""
    
    response = client.chat(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )
    return json.loads(response['message']['content'])

def clasificar_ticket(client, texto, modelo):
    """Quinto análisis obligatorio para el BLOQUE 7"""
    prompt = f"""Clasifica el ticket en formato JSON con:
    - "tema": Categoría técnica.
    - "prioridad": Baja, Media, Alta o Crítica.
    Texto: {texto}"""
    
    response = client.chat(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )
    return json.loads(response['message']['content'])