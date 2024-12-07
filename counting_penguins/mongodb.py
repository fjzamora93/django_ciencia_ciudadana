
from django.conf import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

from bson import ObjectId
import environ

# CARGAR VARIABLES DE ENTORNO
env = environ.Env()
environ.Env.read_env()

# URL de conexión con tu MongoDB Atlas
MONGO_URI = env('MONGO_URI')


# Crear un cliente de MongoDB y conectarse al servidor. La conexión se realiza aquí.
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

DB_NAME = "countingpenguins"
COLLECTION_NAME = "coords"
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





# Ejemplo: Leer y escribir en colecciones
def insertar_dato_en_coleccion(dato:dict) -> int:
    """
    Recibe un dato, ya formateado como json y lo inserta en la base de datos.
    """
    

    dato['tile'] = str(dato['tile'])
    dato['x'] = int(dato['x'])
    dato['y'] = int(dato['y'])

    collection = DB[COLLECTION_NAME]
    result = collection.insert_one(dato)
    print("DATO FORMATEADO: ", dato)
    return result.inserted_id


def clear_tile(tile_name:str):
    """
    Elimina todos los datos de un tile específico. Útil para sobreescribir inmediatamente dentro de un tile.
    """
    collection = DB[COLLECTION_NAME]
    collection.delete_many({'tile': tile_name})



def find_all():
    """
    Obtiene todos los datos de la colección.
    """
    collection = DB[COLLECTION_NAME]
    datos = list(collection.find())
    return datos


def find_by_filter(filtro={}):
    """
    Obtiene las coordenadas directamente de la colección.
    """
    collection = DB[COLLECTION_NAME]
    datos = list(collection.find(filtro))
    return datos


def count_total():
    """
    Cuenta el total de documentos en la colección.
    """
    collection = DB[COLLECTION_NAME]
    total = collection.count_documents({})
    return total

