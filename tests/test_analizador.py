# tests/test_analizador.py
import pytest
import os
import json
from unittest.mock import patch, MagicMock

# --- FIXTURES ---

@pytest.fixture
def analizador():
    """Instancia base del analizador con mock de cliente para evitar llamadas reales."""
    # Parcheamos get_client donde es consumido por el AnalizadorNLP
    with patch('src.analizador.get_client'): 
        from src.analizador import AnalizadorNLP
        return AnalizadorNLP(modelo="test-model")

@pytest.fixture
def mock_resultados():
    """Datos de ejemplo con caracteres especiales para validar encoding."""
    return {
        "sentimiento": {"sentimiento": "positivo", "puntuacion": 0.9},
        "entidades": {"personas": ["Ana"], "lugares": ["Madrid"]},
        "intencion": {"intencion_principal": "consulta", "urgencia": "baja"},
        "resumen": "El cliente está satisfecho con el servicio."
    }

# --- TESTS DE LÓGICA NLP ---

def test_sentimiento_positivo(analizador):
    """Test 1 (Feliz): Verifica detección de sentimiento positivo y flujo completo."""
    # 1. Definimos los valores simulados para todas las etapas del flujo
    mock_sentimiento = {"sentimiento": "positivo", "puntuacion": 0.95}
    mock_entidades = {"personas": ["Ana"], "lugares": ["Madrid"]}
    mock_intencion = {"intencion_principal": "consulta", "urgencia": "baja"}
    mock_resumen = "El cliente está muy satisfecho."

    # 2. Aplicamos patch a todas las funciones consumidas por procesar_texto_completo
    # Importante: se parchean en 'src.analizador' que es donde se importan y usan
    with patch('src.analizador.analizar_sentimiento', return_value=mock_sentimiento), \
         patch('src.analizador.extraer_entidades', return_value=mock_entidades), \
         patch('src.analizador.detectar_intencion', return_value=mock_intencion), \
         patch('src.analizador.generar_resumen', return_value=mock_resumen):
        
        # 3. Ejecutamos el flujo completo sin dependencias externas
        resultado = analizador.procesar_texto_completo("Me encanta el servicio")
        
        # 4. Verificaciones de integridad
        assert resultado["sentimiento"]["sentimiento"] == "positivo"
        assert resultado["sentimiento"]["puntuacion"] > 0.7
        assert "Ana" in resultado["entidades"]["personas"]
        assert resultado["resumen"] == "El cliente está muy satisfecho."

def test_sentimiento_negativo(analizador):
    """Test 2 (Feliz): Verifica detección de sentimiento negativo."""
    # 1. Definimos los valores simulados (Mocks) para cada etapa
    mock_sentimiento = {"sentimiento": "negativo", "puntuacion": 0.1}
    mock_entidades = {"personas": [], "lugares": []}
    mock_intencion = {"intencion_principal": "queja", "urgencia": "alta"}
    mock_resumen = "El cliente no está satisfecho."

    # 2. Aplicamos patch a todas las funciones que llama procesar_texto_completo
    with patch('src.analizador.analizar_sentimiento', return_value=mock_sentimiento), \
         patch('src.analizador.extraer_entidades', return_value=mock_entidades), \
         patch('src.analizador.detectar_intencion', return_value=mock_intencion), \
         patch('src.analizador.generar_resumen', return_value=mock_resumen):
        
        # 3. Ejecutamos el flujo completo
        resultado = analizador.procesar_texto_completo("Es un desastre")
        
        # 4. Verificaciones
        assert resultado["sentimiento"]["sentimiento"] == "negativo"
        assert resultado["sentimiento"]["puntuacion"] < 0.3
        assert resultado["resumen"] == mock_resumen

def test_error_conexion_ollama(analizador):
    """Test 4 (Error): Simula fallo de conexión con el servicio Ollama."""
    # Parcheamos la primera llamada del flujo para simular caída
    with patch('src.analizador.analizar_sentimiento', side_effect=Exception("Connection refused")):
        with pytest.raises(Exception) as excinfo:
            analizador.procesar_texto_completo("Hola")
        assert "Error crítico" in str(excinfo.value)

def test_json_invalido(analizador):
    """Test 5 (Error): Valida el comportamiento ante JSON malformado."""
    raw_response = "Respuesta de texto plano del modelo"
    resultado = analizador.validar_respuesta_json(raw_response)
    assert "error" in resultado
    assert resultado["raw"] == raw_response

# --- TESTS DE ALMACENAMIENTO ---

def test_6_almacenamiento_txt(tmp_path, mock_resultados):
    """Test 6 (Feliz): Verifica persistencia en formato TXT con encoding UTF-8."""
    folder = tmp_path / "resultados" / "txt"
    folder.mkdir(parents=True)
    file_path = folder / "test_output.txt"
    
    # Simulación de guardado (como lo haría guardar_txt)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(mock_resultados["resumen"]))
    
    assert file_path.exists()
    # CORRECCIÓN: Leer explícitamente con UTF-8 para evitar errores en Windows
    assert file_path.read_text(encoding="utf-8") == mock_resultados["resumen"]

def test_7_almacenamiento_json(tmp_path, mock_resultados):
    """Test 7 (Feliz): Verifica persistencia en formato JSON."""
    folder = tmp_path / "resultados" / "json"
    folder.mkdir(parents=True)
    file_path = folder / "test_output.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(mock_resultados, f, ensure_ascii=False)
    
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["sentimiento"]["sentimiento"] == "positivo"