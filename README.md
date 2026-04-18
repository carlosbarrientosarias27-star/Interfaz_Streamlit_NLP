# 🧠 Interfaz Streamlit NLP

![CI Pipeline](https://github.com/<tu-usuario>/INTERFAZ_STREAMLIT_NLP/actions/workflows/CI.yml/badge.svg)

Aplicación web interactiva desarrollada con **Streamlit** para el análisis de texto mediante técnicas de **Procesamiento de Lenguaje Natural (NLP)**. Permite analizar textos en distintos niveles lingüísticos, gestionar el almacenamiento de resultados y visualizar métricas de forma sencilla.

---

## 📋 Descripción

Este proyecto proporciona una interfaz gráfica sobre un motor NLP modular. Las funcionalidades principales incluyen:

- Análisis morfológico, sintáctico y semántico de textos.
- Gestión de resultados: guardar y leer análisis previos.
- Arquitectura por capas separando la lógica (`src/`), la interfaz (`interface/`) y el almacenamiento (`almacenamiento/`).
- Pipeline de integración continua con GitHub Actions.

---

## ⚙️ Instalación

### Requisitos previos

- Python 3.10+ o superior
- pip

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/<tu-usuario>/INTERFAZ_STREAMLIT_NLP.git
cd INTERFAZ_STREAMLIT_NLP

# 2. Crea y activa un entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instala las dependencias (incluye Streamlit)
pip install -r requirements.txt
```

> **Nota:** `requirements.txt` incluye `streamlit` junto con todas las librerías NLP necesarias.

---

## 🚀 Uso

### Ejecutar la aplicación

```bash
streamlit run main.py
```

Se abrirá automáticamente en el navegador en `http://localhost:8501`.

### Ejecutar la demo de interfaz

```bash
streamlit run interface/demo_app.py
```

---

## 🗂️ Estructura de carpetas

```
INTERFAZ_STREAMLIT_NLP/
│
├── .github/
│   └── workflows/
│       └── CI.yml              # Pipeline de integración continua
│
├── almacenamiento/
│   ├── guardar.py              # Lógica de persistencia de resultados
│   └── leer.py                 # Lectura de resultados almacenados
│
├── Heredado/
│   ├── InicialNLP.py           # Versión inicial del motor NLP
│   └── InicialNLPV1.py         # Primera revisión del motor
│
├── interface/
│   └── demo_app.py             # Demo interactiva con Streamlit
│
├── src/
│   ├── analizador.py           # Núcleo del análisis NLP
│   ├── cliente.py              # Capa cliente / entrada de datos
│   ├── niveles.py              # Definición de niveles de análisis
│   └── utils.py                # Utilidades y funciones auxiliares
│
├── tests/
│   ├── test_analizador.py      # Tests del módulo analizador
│   └── test_guardar.py         # Tests del módulo de almacenamiento
│
├── conftest.py                 # Configuración global de pytest
├── main.py                     # Punto de entrada de la aplicación
├── pytest.ini                  # Configuración de pytest
├── requirements.txt            # Dependencias del proyecto
├── baseAlumnos.md              # Base de datos de alumnos (documentación)
└── README.md                   # Este archivo
```

---

## 🧪 Ejecutar los tests

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

El flujo de integración continua se define en `.github/workflows/CI.yml` y se ejecuta automáticamente en cada push o pull request a la rama principal. Incluye:

1. Instalación de dependencias (`pip install -r requirements.txt`).
2. Ejecución de la suite de tests con `pytest`.
3. Reporte del estado del pipeline (badge en este README).

Para actualizar el badge, sustituye `<tu-usuario>` por tu nombre de usuario de GitHub en la URL del badge al inicio de este archivo.

---

## 📄 Licencia

Este proyecto está distribuido bajo los términos recogidos en el archivo [LICENSE](LICENSE).