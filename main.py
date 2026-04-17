import argparse
import sys
from src.analizador import AnalizadorNLP
from src.cliente import check_connection
from almacenamiento.guardar import guardar_json, guardar_txt

def parse_arguments():
    """Configura y gestiona los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(description="Herramienta CLI para análisis NLP con Ollama")
    parser.add_argument(
        "--texto", 
        type=str, 
        help="Texto que se desea analizar entre comillas."
    )
    parser.add_argument(
        "--modelo", 
        type=str, 
        default="qwen2.5:0.5b", 
        help="Modelo de Ollama a utilizar (por defecto: qwen2.5:0.5b)"
    )
    parser.add_argument(
        "--guardar", 
        action="store_true", 
        help="Si se incluye, guarda los resultados en la carpeta resultados/"
    )
    return parser.parse_args()

def run_cli_mode(texto, modelo, guardar):
    """Orquesta la ejecución del análisis en modo consola."""
    if not check_connection():
        print("❌ Error: No se puede conectar con el servidor de Ollama.")
        sys.exit(1)

    print(f"\n{'='*20} INICIANDO ANÁLISIS {'='*20}")
    print(f"Modelo: {modelo}")
    
    analizador = AnalizadorNLP(modelo=modelo)
    
    try:
        # Ejecuta el flujo completo definido en src/analizador.py
        resultados = analizador.procesar_texto_completo(texto)
        
        # Mostrar resultados por consola (Replica la visualización de InicialNLPV1.py)
        print(f"\n🔵 RESUMEN:\n   {resultados.get('resumen')}")
        print(f"\n🔵 SENTIMIENTO: {resultados.get('sentimiento', {}).get('sentimiento')}")
        
        if guardar:
            ruta_json = guardar_json(resultados)
            ruta_txt = guardar_txt(resultados)
            print(f"\n✅ Resultados guardados en:\n   - {ruta_json}\n   - {ruta_txt}")
            
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")

if __name__ == "__main__":
    args = parse_arguments()
    
    # Si el usuario proporciona texto por argumento, se procesa
    if args.texto:
        run_cli_mode(args.texto, args.modelo, args.guardar)
    else:
        # Si no hay argumentos, mostramos ayuda o instrucciones para Streamlit
        print("\n💡 Modo de uso CLI:")
        print('   python main.py --texto "Tu mensaje aquí" --guardar')
        print("\n💡 Modo de uso Web:")
        print("   streamlit run interface/demo_app.py\n")