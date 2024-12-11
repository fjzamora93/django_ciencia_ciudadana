# myapp/utils/tile_management.py

import json
import os
import time
from django.conf import settings

TILES_STATUS_PATH = os.path.join(settings.BASE_DIR, 'static', 'data', 'tiles_status.json')

def load_tile_status():
    """Carga el estado de los tiles desde un archivo JSON."""
    if os.path.exists(TILES_STATUS_PATH):
        with open(TILES_STATUS_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_tile_status(status):
    """Guarda el estado de los tiles en el archivo JSON."""
    with open(TILES_STATUS_PATH, 'w') as f:
        json.dump(status, f, indent=4)

def occupy_tile(tile):
    """Marca un tile como ocupado y guarda el tiempo de ocupación."""
    status = load_tile_status()
    status[tile] = {'status': 'occupied', 'timestamp': time.time()}  # Guardamos el tiempo actual
    save_tile_status(status)

def release_tile(tile):
    """Libera un tile."""
    status = load_tile_status()
    status[tile] = {'status': 'available', 'timestamp': None}
    save_tile_status(status)

def is_tile_available(tile):
    """Comprueba si un tile está disponible o si se debe liberar automáticamente."""
    status = load_tile_status()
    
    # Si el tile no existe o está disponible, retornamos que está disponible
    if tile not in status or status[tile]['status'] == 'available':
        return True

    # Si está ocupado, verificamos si ha pasado el tiempo límite
    timestamp = status[tile]['timestamp']
    if timestamp:
        elapsed_time = time.time() - timestamp
        # Si han pasado más de 2 minutos, liberamos el tile
        if elapsed_time > 120:  # 120 segundos = 2 minutos
            release_tile(tile)
            return True

    return False
