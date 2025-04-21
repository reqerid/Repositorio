# modules/data_loader.py
import json

def cargar_datos(ruta_archivo):
    """
    Carga los datos desde el archivo JSON y retorna una lista.
    Si ocurre algún error, retorna una lista vacía.
    """
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return []
