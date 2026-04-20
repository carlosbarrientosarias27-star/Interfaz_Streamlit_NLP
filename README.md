# 🧠 NLP con Ollama + Streamlit

## 📋 Descripción

Aplicación web interactiva desarrollada con **Streamlit** para el análisis de texto mediante técnicas de **Procesamiento de Lenguaje Natural (NLP)**. Integra modelos de lenguaje vía **Ollama** para ofrecer análisis lingüístico en distintos niveles: morfológico, sintáctico y semántico.

Las funcionalidades principales incluyen:

- Análisis morfológico, sintáctico y semántico de textos en lenguaje natural.
- Almacenamiento automático de resultados en formato **JSON** y **TXT**.
- Arquitectura modular por capas: lógica (`src/`), interfaz (`interface/`), almacenamiento (`almacenamiento/`) y documentación (`docs/`).
- Pipeline de integración continua con **GitHub Actions**.

---

## ⚙️ Instalación

### Requisitos previos

- Python 3.10 o superior
- pip
- [Ollama](https://ollama.com/) instalado y en ejecución local

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/<tu-usuario>/INTERFAZ_STREAMLIT_NLP.git
cd INTERFAZ_STREAMLIT_NLP

# 2. Crea y activa un entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instala las dependencias
pip install streamlit openai python-dotenv
# O bien, instala todas las dependencias del proyecto:
pip install -r requirements.txt
```

> **Nota:** `requirements.txt` incluye `streamlit`, `openai` y `python-dotenv`, junto con todas las librerías NLP necesarias.

---

## 🚀 Uso

### Ejecutar la interfaz web principal

```bash
streamlit run main.py
```

Se abrirá automáticamente en el navegador en `http://localhost:8501`.

### Ejecutar la demo de interfaz

```bash
streamlit run interface/demo_app.py
```

---

## 🗂️ Estructura del proyecto

```
INTERFAZ_STREAMLIT_NLP/
│
├── .github/
│   └── workflows/
│       └── CI.yml                  # Pipeline de integración continua
│
├── almacenamiento/
│   ├── guardar.py                  # Lógica de persistencia de resultados
│   └── leer.py                     # Lectura de resultados almacenados
│
├── docs/
│   ├── almacenamiento.md           # Documentación del módulo de almacenamiento
│   ├── api_referencia.md           # Referencia de la API interna
│   ├── arquitectura.md             # Descripción de la arquitectura del sistema
│   └── streamlit_guia.md          # Guía de uso de la interfaz Streamlit
│
├── Heredado/
│   ├── InicialNLP.py               # Versión inicial del motor NLP
│   └── InicialNLPV1.py             # Primera revisión del motor
│
├── interface/
│   └── demo_app.py                 # Demo interactiva con Streamlit
│
├── logs/
│   └── analisis_YYYYMMDD_*.json    # Registros de análisis por sesión
│
├── Memoria Final/
│   └── Memoria Final.md            # Documentación de la memoria del proyecto
│
├── resultados/
│   ├── json/
│   │   └── analisis_*.json         # Resultados exportados en formato JSON
│   └── txt/
│       └── reporte_*.txt           # Reportes exportados en formato TXT
│
├── src/
│   ├── analizador.py               # Núcleo del análisis NLP
│   ├── cliente.py                  # Capa cliente / entrada de datos
│   ├── niveles.py                  # Definición de niveles de análisis
│   └── utils.py                    # Utilidades y funciones auxiliares
│
├── tests/
│   ├── test_analizador.py          # Tests del módulo analizador
│   └── test_guardar.py             # Tests del módulo de almacenamiento
│
├── conftest.py                     # Configuración global de pytest
├── main.py                         # Punto de entrada de la aplicación
├── pytest.ini                      # Configuración de pytest
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Este archivo
```

---

## 💾 Almacenamiento de resultados

Cada análisis ejecutado se persiste automáticamente en dos formatos y ubicaciones:

### JSON (`resultados/json/` y `logs/`)

Los resultados estructurados se guardan en formato JSON con el siguiente esquema de nombre:

```
analisis_YYYYMMDD_HHMMSS.json
```

Contienen la entrada de texto, los parámetros de análisis seleccionados y la respuesta completa del modelo. La carpeta `logs/` almacena los registros de sesión en tiempo real, mientras que `resultados/json/` guarda las exportaciones manuales del usuario.

### TXT (`resultados/txt/`)

Los reportes en texto plano se generan con el mismo esquema de nombre:

```
reporte_YYYYMMDD_HHMMSS.txt
```

Son versiones legibles del análisis, pensadas para compartir o archivar sin dependencia de herramientas específicas.

La lógica de guardado se encuentra en `almacenamiento/guardar.py` y la de lectura/recuperación en `almacenamiento/leer.py`.

---

## 🧪 Tests

El proyecto usa **pytest**. Para lanzar la suite completa:

```bash
pytest
```

Para ver la salida detallada:

```bash
pytest -v
```

Para ejecutar un módulo de tests específico:

```bash
pytest tests/test_analizador.py
pytest tests/test_guardar.py
```

La configuración de pytest se encuentra en `pytest.ini` y los fixtures compartidos en `conftest.py`.

---

## 🔄 Pipeline CI (GitHub Actions)

El flujo de integración continua se define en `.github/workflows/CI.yml` y se ejecuta automáticamente en cada **push** o **pull request** a la rama principal. Incluye:

1. Instalación de dependencias (`pip install -r requirements.txt`).
2. Ejecución de la suite de tests con `pytest`.
3. Reporte del estado del pipeline mediante el badge en la cabecera de este README.

> Para activar el badge, sustituye `<tu-usuario>` por tu nombre de usuario de GitHub en la URL del badge al inicio de este archivo.

---

## 📄 Licencia

Este proyecto está distribuido bajo los términos recogidos en el archivo [LICENSE](LICENSE).