
from django.conf import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

from bson import ObjectId
import environ

import counting_penguins.utils.coords_converter as coords_converter


# CARGAR VARIABLES DE ENTORNO
env = environ.Env()
environ.Env.read_env()

# URL de conexión con tu MongoDB Atlas
MONGO_URI = env('MONGO_URI')


# Crear un cliente de MongoDB y conectarse al servidor. La conexión se realiza aquí.
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

DB_NAME = "countingpenguins"

PIXEL_COORDS_COLLECTION = "pixels_coords"
GEO_COORDS_COLLECTION = "geo_coords"
NO_PENGUINS_COLLECTION = "tiles_without_penguin"


DB = client[DB_NAME]

def test_connection():
    """
    Únicamente prueba la conexión a la base de datos, no hace nada más.
    """
    try:
        client.admin.command('ping')
        print("\n¡Conexión exitosa con MongoDB!")
    except Exception as e:
        print(f"Error de conexión: {e}")


def classify_tile_without_penguin(dato:dict) -> int:
    """
    Recibe un dato, ya formateado como json y lo inserta en la colección donde están los tiles sin pingüinos.
    """
    collection = DB[NO_PENGUINS_COLLECTION]
    result = collection.insert_one(dato)
    print("No hay pinguinos")

    return result.inserted_id


def insert_many_coords(data_list: list[dict]) -> list[ObjectId]:
    """
    Recibe una lista de dict ya parseada y lo inserta en la base de datos.
    Estas coordenadas ya están formateadas para entrenar el modelo de IA
    (solamente sería necesario normalizarlas antes de pasarlas al yolo).

    Args:
    - data_list: Lista de diccionarios con las coordenadas de los pixeles.
    """
    collection = DB[PIXEL_COORDS_COLLECTION]
    result = collection.insert_many(data_list)
    return result.inserted_ids


def clear_tile(tile_name:str):
    """
    Elimina todos los datos de un tile específico. Útil para sobreescribir inmediatamente dentro de un tile.
    """
    collection = DB[PIXEL_COORDS_COLLECTION]
    collection_without_penguins = DB[NO_PENGUINS_COLLECTION]
    collection_without_penguins.delete_many({'tile': tile_name})
    collection.delete_many({'tile': tile_name})



def find_all():
    """
    Obtiene todos los datos de la colección.
    """
    collection = DB[PIXEL_COORDS_COLLECTION]
    datos = list(collection.find())
    return datos


def find_by_filter(filtro={}):
    """
    Obtiene las coordenadas directamente de la colección.
    """
    collection = DB[PIXEL_COORDS_COLLECTION]
    datos = list(collection.find(filtro))
    return datos


def count_total():
    """
    Cuenta el total de documentos en la colección.
    """
    collection = DB[PIXEL_COORDS_COLLECTION]
    total = collection.count_documents({})
    return total


def already_marked(tile_name:str) -> bool:
    """
    Verifica si un tile está disponible.
    """
    collection = DB[PIXEL_COORDS_COLLECTION]
    total = collection.count_documents({'tile': tile_name})

    no_penguins_collect = DB[NO_PENGUINS_COLLECTION]
    total_no_penguins = no_penguins_collect.count_documents({'tile': tile_name})

    is_available = total == 0 and total_no_penguins == 0
    print("Evaluando disponibilidad del tile: ", is_available)
    return is_available



#! Leer función antes de usarla
def insert_pixel_to_coordinates(coords_list: list[dict]) -> bool:
    """
    Convierte las coordenadas de los pixeles a coordenadas geográficas y las inserta en la base de datos.

    Usar esta función requiere de lo siguiente:
    - Dentro de la static/data/ se debe tener un archivo CSV con las coordenadas de las esquinas de las imágenes.
    - Dentro de la static/img/ se deben tener los archivos TIFF.

    Si dentro del csv con los corners NO está la imagen que esté analizando, se lanzará un error.
    """
    collection = DB[GEO_COORDS_COLLECTION]
    geo_coords = []

    for coord in coords_list:
        print("Convirtiendo coordenadas...: ", coord)
        geo_x, geo_y = coords_converter.pixel_to_coordinates(
            tile_name = coord['tile'], 
            pixel_x = coord['x_center'], 
            pixel_y = coord['y_center']
        )
        geo_coords.append({
            'class': coord['class'],
            'x_center': geo_x,
            'y_center': geo_y,
            'width': coord['width'],
            'height': coord['height'],
            'tile': coord['tile'], 
        })

    collection.insert_many(geo_coords)
    return True