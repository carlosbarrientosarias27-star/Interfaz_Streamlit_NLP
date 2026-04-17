import json

def obtener_sentimiento(client, texto, modelo):
    system_prompt = """Analiza el sentimiento. Responde ÚNICAMENTE en JSON: 
    {"sentimiento": "positivo/negativo/neutral", "puntuacion": 0.0-1.0, "emociones": []}"""
    
    response = client.chat(model=modelo, messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": texto}
    ], format="json")
    return json.loads(response['message']['content'])

def extraer_entidades(client, texto, modelo):
    system_prompt = "Extrae entidades. Responde ÚNICAMENTE en JSON: {personas:[], lugares:[], fechas:[]}"
    response = client.chat(model=modelo, messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": texto}
    ], format="json")
    return json.loads(response['message']['content'])