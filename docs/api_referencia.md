# Referencia de la API Interna

Este documento proporciona una guía técnica de las funciones principales contenidas en el núcleo del proyecto (`src/`). Está diseñado para desarrolladores que necesiten integrar nuevas funciones o realizar mantenimiento.

---

## 1. Módulo: `analizador.py`
Es el orquestador principal que gestiona la comunicación con el modelo de lenguaje (Ollama).

### `ejecutar_analisis(texto, cliente_id, nivel_id)`
Envía una petición al modelo y procesa la respuesta.

* **Parámetros:**
    * `texto` (str): El contenido textual a analizar.
    * `cliente_id` (str): Identificador del cliente para el contexto del prompt.
    * `nivel_id` (int): Nivel de profundidad del análisis solicitado.
* **Retorno:** `dict` - Un diccionario con el resultado estructurado (entidades, sentimiento, resumen).
* **Excepciones:** * `ConnectionError`: Si el servidor local de Ollama no está activo.
    * `ValueError`: Si el texto está vacío o el nivel no es válido.

---

## 2. Módulo: `cliente.py`
Gestiona la información y el contexto específico de los clientes.

### `obtener_datos_cliente(cliente_id)`
Recupera los metadatos asociados a un cliente específico.

* **Parámetros:**
    * `cliente_id` (str): El nombre o clave del cliente.
* **Retorno:** `dict` - Diccionario con preferencias del cliente (ej. idioma, sector industrial).
* **Excepciones:** * `KeyError`: Si el cliente no existe en la base de datos o archivo de configuración.

### `listar_clientes()`
Devuelve la lista de todos los clientes registrados.

* **Retorno:** `list[str]` - Lista de nombres de clientes.

---

## 3. Módulo: `niveles.py`
Define la complejidad y el tipo de procesamiento que realizará la IA.

### `obtener_prompt_por_nivel(nivel_id)`
Carga la plantilla de instrucciones (System Prompt) según el nivel de análisis.

* **Parámetros:**
    * `nivel_id` (int): Nivel solicitado (1: Básico, 2: Intermedio, 3: Avanzado).
* **Retorno:** `str` - La cadena de texto con las instrucciones para el modelo.
* **Excepciones:** * `IndexError`: Si el nivel solicitado no está definido en el sistema.

### `validar_configuracion_nivel(nivel_id)`
Verifica que el nivel seleccionado sea compatible con el modelo cargado actualmente.

* **Retorno:** `bool` - True si es válido.

---

## Resumen de Excepciones Comunes

| Excepción | Causa | Manejo sugerido |
| :--- | :--- | :--- |
| `OllamaServerTimeout` | El modelo tarda demasiado en responder. | Mostrar mensaje de espera en Streamlit. |
| `InvalidResponseFormat` | La respuesta de la IA no es un JSON válido. | Reintentar la petición o usar `utils.py` para limpiar. |
| `FileSystemError` | Error al intentar acceder a los archivos de configuración. | Verificar permisos de lectura en la carpeta `src/`. |

---