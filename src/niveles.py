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
    response = client.chat(
        model=modelo,
        messages=[
            {"role": "system", "content": "Resume el texto en una sola frase potente."},
            {"role": "user", "content": texto}
        ]
    )
    return response['message']['content'].strip()