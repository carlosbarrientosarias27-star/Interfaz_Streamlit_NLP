import pytest
import json
import os
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime
from src.analizador import AnalizadorNLP

# --- FIXTURES ---

@pytest.fixture
def mock_functions():
    """Mockea todas las funciones importadas de src.niveles"""
    with patch('src.analizador.analizar_sentimiento') as m_sent, \
         patch('src.analizador.extraer_entidades') as m_ent, \
         patch('src.analizador.detectar_intencion') as m_int, \
         patch('src.analizador.generar_resumen') as m_res, \
         patch('src.analizador.clasificar_ticket') as m_clas:
        
        m_sent.return_value = "positivo"
        m_ent.return_value = ["entidad1"]
        m_int.return_value = "queja"
        m_res.return_value = "resumen corto"
        m_clas.return_value = "soporte"
        
        yield {
            "sentimiento": m_sent,
            "entidades": m_ent,
            "intencion": m_int,
            "resumen": m_res,
            "clasificacion": m_clas
        }

@pytest.fixture
def analizador():
    """Instancia del analizador con el cliente mockeado"""
    with patch('src.cliente.get_client'):
        return AnalizadorNLP(modelo="test-model")

# --- TESTS ---

def test_procesar_texto_completo_success(analizador, mock_functions):
    """
    Test 1 (Feliz): Verifica que el flujo orquestador funcione y 
    devuelva todas las claves esperadas.
    """
    texto = "Excelente servicio al cliente"
    
    # Usamos 'as m_guardar' para capturar el mock creado por patch.object
    with patch.object(analizador, 'guardar_en_log') as m_guardar:
        resultado = analizador.procesar_texto_completo(texto)
    
    # Verificaciones de contenido
    assert "sentimiento" in resultado
    assert "entidades" in resultado
    assert resultado["sentimiento"] == "positivo"
    
    # Verificamos la llamada usando la variable m_guardar
    assert m_guardar.called is True
    # O mejor aún, verifica que se llamó con los resultados
    m_guardar.assert_called_once_with(resultado)

def test_guardar_en_log_formato(analizador):
    """
    Test 2 (Feliz): Valida que se cree el directorio y el archivo 
    JSON con el formato de nombre correcto.
    """
    datos = {"test": "data"}
    # Mockeamos os.makedirs y open para no tocar el disco real
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs') as m_makedirs, \
         patch('builtins.open', mock_open()) as m_file:
        
        path_generado = analizador.guardar_en_log(datos)
        
        m_makedirs.assert_called_once_with('logs')
        assert "logs/analisis_" in path_generado
        assert path_generado.endswith(".json")

def test_cambio_modelo_constructor():
    """
    Test 3 (Borde): Verifica que el modelo inyectado sea el que se usa.
    """
    modelo_custom = "deepseek-v3"
    with patch('src.cliente.get_client'):
        instancia = AnalizadorNLP(modelo=modelo_custom)
        assert instancia.modelo == modelo_custom

def test_texto_entrada_vacio(analizador, mock_functions):
    """
    Test 4 (Borde): Verifica comportamiento ante entrada vacía.
    """
    with patch.object(analizador, 'guardar_en_log'):
        resultado = analizador.procesar_texto_completo("")
    
    # El sistema debe procesar aunque el texto sea vacío
    assert "sentimiento" in resultado
    mock_functions["sentimiento"].assert_called_with(analizador.client, "", analizador.modelo)

def test_error_en_procesamiento(analizador, mock_functions):
    """
    Test 5 (Error): Simula una falla de conexión/API en las funciones de NLP.
    """
    # Forzamos una excepción en una de las funciones mockeadas
    mock_functions["sentimiento"].side_effect = Exception("Conexión fallida con Ollama")
    
    resultado = analizador.procesar_texto_completo("Cualquier texto")
    
    assert "error" in resultado
    assert "Conexión fallida con Ollama" in resultado["error"]

def test_error_permisos_logs(analizador, mock_functions):
    """
    Test 6 (Error): Simula error de permisos asegurando que se intente crear la carpeta.
    """
    # Forzamos a que crea que la carpeta NO existe y que falle al intentar crearla
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs', side_effect=PermissionError("Acceso denegado")):
        
        resultado = analizador.procesar_texto_completo("Test de error")
        
        assert "error" in resultado
        assert "Acceso denegado" in resultado["error"]