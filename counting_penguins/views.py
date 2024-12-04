from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import json
import os
import pandas as pd
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from .mongodb import *


prefix = 'subrecorte'

def hola_mundo(request):
    #next_tile = increment_tile(f'{prefix}_1')
    next_tile = 'subrecorte_9'
    return redirect(f'/{next_tile}')



def save_coords(request):
    if request.method == 'POST':
        try:
            current_tile = request.POST.get('tile', '{prefix}_0')
            clear_tile(current_tile)
            
            coords_list = json.loads(request.POST.get('coords', '[]'))
            for coord in coords_list:
                print("Coordenada a insertar", coord)
                insertar_dato_en_coleccion(coord)
            

            print(coords_list)

            

            next_tile = increment_tile(current_tile)  
            print("Redirigiendo a ", next_tile, " desde el tile actual que es: ", current_tile)
            return redirect(reverse('navigate_to_tile', args=[next_tile]))

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)


def navigate_to_tile(request, tile):
    test_connection()
    print(f"Valor de tile recibido: {tile}")
    coords = []
    if '_' in tile:
        try:
            number = tile.split('_')[1]
        except IndexError:
            return JsonResponse({'message': 'Invalid tile format'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid tile format'}, status=400)
        
    coords = find_by_filter({'tile': tile})
    print(coords)
    
    return render(request, 'index.html', {
        'tile': tile,
        'number' : number,
        'coords': coords
        })


def increment_tile(current_tile):
    """
    Calcula el siguiente tile basado en los siguientes criterios:
    - El primer tile disponible (verificar si el tile 1 existe, si no existe, pasa al siguiente).
    - El tile no puede tener ninguna entrada dentro de static/data/coords.json. Si el tile está marcado, se pasará al siguiente (se suma +1)
    - Si el siguiente tile no existe dentro de la carpeta static/img, se pasará al siguiente (se suma +1)

    Ejemplo: 'tile_9' -> 'tile_10'.
    Si el 10 no existe, se pasará al 11, y así sucesivamente.
    Si el 10 existe dentro de static/data/coords.json, se pasará al 11, y así sucesivamente.

    Si no existen más tiles, aparecerá un mensaje de que no quedan más tiles disponibles.
    """


    prefix, number = current_tile.rsplit('_', 1)
    next_number = int(number) + 1
    contador = 0

    while True:
        if next_number > 500:
            break
        print("Número actual", next_number)

        next_tile = f'{prefix}_{next_number}'
        img_path = os.path.join(settings.BASE_DIR, 'static', 'img', f'{next_tile}.jpg')
        coords_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'coords.json')

        if not os.path.exists(img_path):
            next_number += 1
            continue

        with open(coords_path, 'r') as f:
            coords_data = json.load(f)
            if next_tile not in coords_data:
                return next_tile

        next_number += 1

        

    return None




def no_more_tiles():
    return render(request, 'no_more_tiles.html', {})