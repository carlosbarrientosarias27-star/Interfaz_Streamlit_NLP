import pytest
import os
import json
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime
from guardar import guardar_json, guardar_txt, JSON_DIR, TXT_DIR, BASE_DIR

# --- FIXTURES PARA SETUP & TEARDOWN ---

@pytest.fixture(autouse=True)
def setup_teardown():
    """Limpia el directorio de resultados antes y después de cada test."""
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)
    yield
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)

@pytest.fixture
def mock_ollama_data():
    """Simula el diccionario que devolvería un análisis NLP de Ollama."""
    return {
        "resumen": "El cliente reporta una falla en el servidor tras la actualización.",
        "sentimiento": {"sentimiento": "negativo", "confianza": 0.89},
        "entidades": {
            "PROD": ["Servidor", "Software"],
            "ORG": ["IT Dept"]
        }
    }

# --- PRUEBAS UNITARIAS ---

class TestGuardarModulo:

    # --- CASOS FELICES ---
    
    def test_guardar_json_exitoso(self, mock_ollama_data):
        """Verifica que el JSON se guarde con el contenido correcto y en la ruta definida."""
        ruta = guardar_json(mock_ollama_data)
        
        assert ruta is not None
        assert os.path.exists(ruta)
        assert ruta.startswith(JSON_DIR)
        
        with open(ruta, 'r', encoding='utf-8') as f:
            datos_cargados = json.load(f)
            assert datos_cargados["resumen"] == mock_ollama_data["resumen"]

    def test_guardar_txt_exitoso(self, mock_ollama_data):
        """Valida que el reporte legible se genere con el formato esperado."""
        ruta = guardar_txt(mock_ollama_data)
        
        assert ruta is not None
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            assert "REPORTE DE ANÁLISIS NLP" in contenido
            assert "📊 SENTIMIENTO: NEGATIVO" in contenido
            assert "Confianza: 89.0%" in contenido

    # --- CASOS BORDE (EDGE CASES) ---

    def test_guardar_datos_vacios(self):
        """Verifica el comportamiento cuando los datos de la IA vienen incompletos."""
        datos_vacios = {"entidades": {}} # Faltan llaves de resumen y sentimiento
        ruta = guardar_txt(datos_vacios)
        
        assert ruta is not None
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            assert "📝 RESUMEN:\nSin resumen" in contenido
            assert "📊 SENTIMIENTO: N/A" in contenido

    def test_guardar_entidades_tipo_mixto(self):
        """Caso borde: entidades con valores numéricos o nulos."""
        datos = {
            "entidades": {"IDs": [123, 456], "Status": [None]}
        }
        ruta = guardar_txt(datos)
        assert ruta is not None
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
            assert "123, 456" in contenido
            assert "None" in contenido

    # --- CASOS DE ERROR & MOCKS DE OLLAMA ---

    @patch('ollama.chat') # Simulamos la llamada a la API externa
    def test_flujo_completo_con_mock_ollama(self, mock_ollama, mock_ollama_data):
        """
        Simula una llamada exitosa a Ollama y el guardado posterior.
        """
        # Configuramos el mock para que devuelva un objeto con .message.content
        mock_response = MagicMock()
        mock_response.message.content = json.dumps(mock_ollama_data)
        mock_ollama.return_value = mock_response

        # Ejecución simulada
        response = mock_ollama("llama3", messages=[])
        data_procesada = json.loads(response.message.content)
        ruta = guardar_json(data_procesada)
        
        assert ruta is not None
        assert os.path.exists(ruta)

    @patch('builtins.open', side_effect=PermissionError("Acceso denegado"))
    def test_error_permisos_escritura(self, mock_open, mock_ollama_data):
        """Caso de Error: El sistema no tiene permisos para escribir en el disco."""
        ruta = guardar_json(mock_ollama_data)
        assert ruta is None # La función captura la excepción y retorna None