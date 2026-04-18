# Documentación del Sistema de Almacenamiento

Este documento describe el funcionamiento de los módulos de persistencia de datos situados en la carpeta `almacenamiento/`, así como la estructura de los archivos generados por el sistema.

## 1. Módulos de Persistencia

El sistema utiliza dos scripts principales para gestionar el ciclo de vida de los datos:

* **`guardar.py`**: Se encarga de recibir los objetos procesados por el `analizador.py`, formatearlos y escribirlos en el disco. Implementa la lógica de creación de carpetas automáticas y manejo de colisiones de nombres.
* **`leer.py`**: Proporciona funciones para recuperar análisis previos, permitiendo que la interfaz de Streamlit cargue el historial o retome sesiones de trabajo anteriores.

---

## 2. Formato de Archivos JSON

Los archivos JSON se utilizan para el almacenamiento de datos estructurados, facilitando su posterior procesamiento por otras herramientas o la propia aplicación.

### Esquema del JSON
Cada archivo generado sigue esta estructura de claves:

| Clave | Tipo | Descripción |
| :--- | :--- | :--- |
| `id_analisis` | `string (UUID)` | Identificador único universal del análisis. |
| `fecha` | `string (ISO 8601)` | Marca de tiempo de la ejecución (YYYY-MM-DD HH:MM:SS). |
| `cliente` | `string` | Nombre o ID del cliente asociado al texto. |
| `nivel` | `integer` | Nivel de profundidad del análisis (1, 2 o 3). |
| `entrada` | `string` | El texto original enviado a Ollama. |
| `resultado` | `object` | Objeto que contiene las entidades extraídas y el resumen. |
| `tokens` | `integer` | Cantidad aproximada de tokens procesados (si aplica). |

**Ejemplo de contenido:**
```json
{
  "id_analisis": "550e8400-e29b-41d4-a716-446655440000",
  "fecha": "2026-04-18 10:30:15",
  "cliente": "Empresa_ABC",
  "nivel": 2,
  "entrada": "Texto de ejemplo