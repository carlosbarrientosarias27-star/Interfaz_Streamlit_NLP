# Arquitectura del Proyecto: NLP con Ollama + Streamlit

Este documento detalla la estructura organizativa del proyecto y el flujo de información entre sus componentes, desde la interacción del usuario hasta el procesamiento por el Modelo de Lenguaje (LLM).

---

## 1. Jerarquía del Proyecto

El sistema está diseñado siguiendo una separación de responsabilidades para facilitar el mantenimiento y la escalabilidad:

* **`interface/`**: Capa de presentación (Frontend). Contiene la lógica visual y captura de eventos del usuario.
* **`src/`**: Núcleo de la aplicación (Backend). Procesa la lógica de negocio, gestiona el filtrado de datos y coordina la comunicación con el motor de IA.
* **`almacenamiento/`**: Capa de persistencia. Gestiona la escritura y lectura de archivos físicos (JSON/TXT).
* **`tests/`**: Suite de validación para garantizar que los cambios en el código no rompan funcionalidades existentes.
* **`.github/workflows/`**: Automatización de procesos (CI) para asegurar la calidad del código en cada commit.

---

## 2. Flujo de Datos

El flujo de información sigue un camino lineal y controlado:

1.  **Entrada:** El usuario introduce un texto y selecciona parámetros (Cliente/Nivel) en `interface/demo_app.py`.
2.  **Solicitud:** La interfaz invoca las funciones de `src/analizador.py`.
3.  **Contexto:** `analizador.py` solicita datos adicionales a `src/cliente.py` y define las instrucciones del prompt según `src/niveles.py`.
4.  **Inferencia:** El sistema envía la petición procesada a **Ollama** a través de su API local.
5.  **Respuesta:** Ollama devuelve el resultado, el cual es limpiado y estructurado por `src/utils.py`.
6.  **Persistencia:** Los datos finales se envían a `almacenamiento/guardar.py` para su registro en disco.
7.  **Salida:** Streamlit renderiza el resultado final y los metadatos en pantalla para el usuario.

---

## 3. Diagrama de Arquitectura

```mermaid
graph TD
    User((Usuario)) -->|Interactúa| UI[interface/demo_app.py]
    
    subgraph Backend [Logic Layer - src]
        UI --> Analizador[analizador.py]
        Analizador --> Cliente[cliente.py]
        Analizador --> Niveles[niveles.py]
        Analizador --> Utils[utils.py]
    end
    
    subgraph AI_Engine [Local Engine]
        Analizador <-->|API Request/Response| Ollama[Ollama LLM]
    end
    
    subgraph Storage [Data Layer]
        Analizador --> Guardar[almacenamiento/guardar.py]
        Guardar --> JSON[(Resultados JSON)]
        Guardar --> TXT[(Reportes TXT)]
    end
    
    Analizador -->|Retorna Datos| UI