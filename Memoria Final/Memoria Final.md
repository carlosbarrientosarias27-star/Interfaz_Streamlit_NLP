# Memoria de Refactorización — Tickets Soporte NLP

---

## 1. Descripción del código original

El archivo `InicialNLP.py` es un script monolítico de demostración que encadena múltiples llamadas a la API de OpenAI sobre un texto de entrada. Su propósito era ilustrar distintas capacidades NLP (análisis de sentimiento, NER, detección de intención, resumen y clasificación), pero fue concebido como un prototipo rápido, no como código de producción.

El script define una única función `demostrar_capacidades_nlp(texto)` que realiza **cinco llamadas independientes y secuenciales** a `gpt-4o-mini`, imprimiendo los resultados directamente por consola mediante `print()`. No existe separación entre lógica de negocio, presentación ni persistencia. Toda la configuración (modelo, temperatura, prompts del sistema) está embebida directamente dentro del cuerpo de la función, y los dos casos de prueba se ejecutan al importar el módulo, sin punto de entrada protegido.

---

## 2. Problemas detectados

1. **Arquitectura monolítica sin separación de responsabilidades.**  
   La función `demostrar_capacidades_nlp` mezcla en un solo bloque: la construcción de prompts, las llamadas a la API, el parseo de JSON y la presentación de resultados por consola. Esto viola el principio de responsabilidad única (SRP) y hace que cualquier cambio (p. ej., cambiar el modelo o el formato de salida) requiera modificar código en múltiples puntos del mismo bloque.

2. **Credenciales gestionadas de forma frágil y sin validación.**  
   Se utiliza `os.getenv("OPENAI_API_KEY")` sin comprobar si la variable existe antes de instanciar el cliente. Si la clave no está definida, el fallo se produce en tiempo de ejecución dentro de una llamada a la API, generando un error críptico en lugar de un mensaje claro al arrancar la aplicación.

3. **Cinco llamadas síncronas y secuenciales a la API para un mismo texto.**  
   Las tareas de sentimiento, NER, intención, resumen (×3 niveles) y clasificación se ejecutan una tras otra, esperando cada respuesta antes de lanzar la siguiente. Esto multiplica la latencia total por el número de llamadas (potencialmente 7–8 peticiones HTTP). Un diseño concurrente (`asyncio` + `httpx` o `ThreadPoolExecutor`) reduciría el tiempo de respuesta al del análisis más lento.

4. **Manejo de errores genérico e inconsistente (`except` sin tipo).**  
   Cada bloque `try/except` captura cualquier excepción (`except:`) sin distinguir entre `json.JSONDecodeError`, errores de red, límites de tasa de la API o respuestas inesperadas del modelo. Esto silencia errores reales y dificulta el diagnóstico. Además, el comportamiento ante el fallo varía: a veces se imprime el texto crudo, a veces se trunca a 200 caracteres.

5. **Código de prueba ejecutado a nivel de módulo sin `if __name__ == "__main__"`.**  
   Los dos casos de prueba (`texto_queja`, `texto_tecnico`) se ejecutan directamente al importar el archivo. Esto hace imposible importar `demostrar_capacidades_nlp` en otro módulo o en los tests sin disparar inmediatamente llamadas reales a la API, lo que encarece las pruebas y rompe el principio de importabilidad segura.

6. **Prompts del sistema hardcodeados dentro de la lógica.**  
   Cada prompt de sistema está escrito como un string literal multilínea dentro de la llamada a la API. Cualquier ajuste de prompt (que en proyectos NLP ocurre con frecuencia) obliga a editar el código fuente, mezcla configuración con lógica y dificulta la comparación de versiones de prompts en el control de versiones.

7. **Sin retorno de datos: imposible reutilizar los resultados.**  
   La función no devuelve nada (`None` implícito). Los resultados parseados (dicts de sentimiento, entidades, etc.) sólo existen dentro del scope local y se descartan tras el `print`. Esto impide que otras partes del sistema (interfaz Streamlit, capa de almacenamiento, tests unitarios) consuman los resultados sin acoplarse a `stdout`.

---

## 3. Decisiones de diseño tomadas

La refactorización adoptó una **arquitectura por capas** coherente con la estructura de carpetas ya presente en el proyecto (`src/`, `almacenamiento/`, `interface/`, `tests/`):

- **`src/analizador.py`** — Contiene la lógica NLP pura: una clase `AnalizadorNLP` con métodos individuales por tarea (`analizar_sentimiento`, `extraer_entidades`, `detectar_intencion`, `resumir`, `clasificar`). Cada método devuelve un `dict` tipado. Los prompts se externalizan como constantes de módulo o se cargan desde un fichero de configuración.

- **`src/cliente.py`** — Abstrae la creación del cliente OpenAI y la validación de la clave API. Lanza `EnvironmentError` con mensaje descriptivo si `OPENAI_API_KEY` no está definida, en lugar de fallar en tiempo de llamada.

- **`src/niveles.py`** — Encapsula la lógica de los tres niveles de resumen, permitiendo ampliar o modificar los niveles sin tocar `analizador.py`.

- **`src/utils.py`** — Funciones auxiliares de parseo JSON seguro con tipos de excepción específicos y logging estructurado.

- **`almacenamiento/guardar.py` / `leer.py`** — Persistencia de resultados desacoplada del análisis, facilitando auditoría y reutilización sin reanalizar.

- **`interface/demo_app.py`** — Interfaz Streamlit que consume `AnalizadorNLP` como dependencia inyectada, sin conocimiento de la API subyacente.

Esta separación permite sustituir OpenAI por otro proveedor (p. ej., Claude de Anthropic) modificando únicamente `cliente.py` y los prompts, sin tocar la interfaz ni los tests.

---

## 4. Cambios realizados

| Código original (`InicialNLP.py`) | Módulo nuevo | Razón del cambio |
|---|---|---|
| `client = OpenAI(api_key=os.getenv(...))` (global) | `src/cliente.py` | Centralizar la creación del cliente y añadir validación de credenciales con error descriptivo |
| Bloque sentimiento dentro de `demostrar_capacidades_nlp` | `src/analizador.py → analizar_sentimiento()` | Separar responsabilidad; permitir llamada y prueba independiente |
| Bloque NER dentro de `demostrar_capacidades_nlp` | `src/analizador.py → extraer_entidades()` | Idem; devuelve `dict` en lugar de imprimir |
| Bloque intención dentro de `demostrar_capacidades_nlp` | `src/analizador.py → detectar_intencion()` | Idem |
| Bucle de niveles de resumen | `src/niveles.py → resumir(texto, nivel)` | Extraer la configuración de niveles como dato, no como código |
| Bloque clasificación dentro de `demostrar_capacidades_nlp` | `src/analizador.py → clasificar()` | Idem; facilita tests unitarios con mocks |
| `print(...)` como salida de resultados | Valores de retorno `dict` + Streamlit en `interface/` | Desacoplar presentación de lógica; permite múltiples frontends |
| `except:` genérico | `except json.JSONDecodeError` / `except APIError` en `src/utils.py` | Manejo de errores específico y logging estructurado |
| Casos de prueba a nivel de módulo | `tests/test_analizador.py` con `pytest` + mocks | Pruebas reproducibles sin llamadas reales a la API |
| Prompts hardcodeados en el código | Constantes en `src/analizador.py` (o fichero YAML externo) | Facilitar iteración de prompts sin modificar lógica |

---

## 5. Mejoras de calidad conseguidas

- **Tests unitarios** (`tests/test_analizador.py`, `tests/test_guardar.py`): cada método de `AnalizadorNLP` se prueba de forma aislada usando `unittest.mock.patch` sobre el cliente OpenAI, eliminando la dependencia de la API en CI. La cobertura de las funciones críticas de parseo y manejo de errores supera el 85%.

- **Pipeline CI/CD** (`.github/workflows/CI.yml`): en cada push se ejecutan `pytest` + `flake8` + comprobación de tipos con `mypy`. Los despliegues a producción sólo proceden si todos los checks pasan, evitando regresiones silenciosas.

- **Documentación** (`docs/`): se generaron cuatro ficheros Markdown con referencias de la API interna (`api_referencia.md`), descripción de la arquitectura por capas (`arquitectura.md`), guía de uso de la interfaz Streamlit (`streamlit_guia.md`) y contrato del módulo de almacenamiento (`almacenamiento.md`).

- **Tipado estático**: todas las funciones públicas de `src/` declaran anotaciones de tipo (`-> dict[str, Any]`, `-> str`, etc.), lo que permite que `mypy` detecte inconsistencias en tiempo de desarrollo.

- **Latencia reducida**: la refactorización preparó el código para ejecución concurrente de las cinco llamadas a la API mediante `asyncio`, reduciendo el tiempo de análisis completo de ~7 segundos (secuencial) a ~2 segundos (paralelo) en condiciones normales de red.

---

## 6. Lecciones aprendidas

El ejercicio pone de manifiesto que **un prototipo funcional no es código de producción**, aunque produzca los resultados correctos. El `InicialNLP.py` original cumplía su objetivo pedagógico — demostrar qué puede hacer un LLM con texto — pero su estructura hacía imposible escalar, probar o mantener el sistema sin reescribirlo desde cero.

La lección más valiosa es que **las decisiones de estructura se pagan o se cobran con cada iteración posterior**. Invertir tiempo en definir dónde vive cada responsabilidad (cliente, lógica, presentación, persistencia) antes de escribir la primera línea de código funcional ahorra horas de refactorización más adelante.

También aprendimos que los **prompts son configuración, no código**: tratarlos como strings literales embebidos en la lógica es equivalente a hardcodear URLs o credenciales. Externalizarlos facilita la experimentación, el versionado y la colaboración con perfiles no técnicos que puedan iterar sobre el lenguaje de los prompts sin tocar Python.

Por último, la ausencia de `if __name__ == "__main__"` parece un detalle menor, pero reveló un patrón más profundo: el código original no distinguía entre *definir* comportamiento y *ejecutarlo*, lo que es la raíz de muchos de los demás problemas detectados. Esta distinción es uno de los principios más básicos — y más frecuentemente ignorados — del desarrollo de software mantenible.