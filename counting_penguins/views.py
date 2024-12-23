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
from . import mongodb as db

from counting_penguins.utils.tile_management import *


prefix = 'subrecorte'


def home(request):
    all_penguins_done = request.session.get('all_penguins_done', False) 

    if request.method == 'POST':
        repeat_marked = request.POST.get('repeat_marked') == 'true'
        request.session['repeat_marked'] = repeat_marked
    else:
        repeat_marked = request.session.get('repeat_marked', True)
    
    num_penguins = count_total()
    return render(request, 'index.html', {
        'count': num_penguins,
        'repeat_marked': repeat_marked,
        'all_penguins_done': all_penguins_done
    })

def find_tile(request):
    repeat_marked = request.GET.get("repeat_marked") == "true"
    request.session['repeat_marked'] = repeat_marked
    next_tile = increment_tile(request,f'{prefix}_1')
    return redirect(f'/{next_tile}')
 

def save_coords(request):

    current_tile = request.POST.get('tile', '{prefix}_0')
    next_tile = increment_tile(request, current_tile)
    to_save = request.POST.get('save') == "true"  
    no_penguins = request.POST.get('save') == "no-penguins"
    if request.method == 'POST':
        if to_save:
            clear_tile(current_tile)
            coords_list = json.loads(request.POST.get('coords', '[]'))
            
            if len(coords_list) > 0:
                insert_many_coords(coords_list) 

            #! Hacemos la inserción en la colección con georeferencia
            #insert_pixel_to_coordinates(coords_list)
        elif no_penguins:
            clear_tile(current_tile)
            db.classify_tile_without_penguin({
                'tile': current_tile,
                'has_penguin': False
            })
    return redirect(reverse('navigate_to_tile', args=[next_tile]))

   

def navigate_to_tile(request, tile):
    if '_' in tile:
        number = tile.split('_')[1]
    else:
        return JsonResponse({'message': 'Invalid tile format'}, status=400)
  
    # Si no está disponible, redirigir al siguiente tile
    # if not is_tile_available(tile):
    #     next_tile = increment_tile(tile)
    #     return redirect(reverse('navigate_to_tile', args=[next_tile]))
    
    # Verificar que está activada la función de repetir tiles
    if not db.already_marked(tile) and not request.session.get('repeat_marked'):
        next_tile = increment_tile(request, tile)
        return redirect(reverse('navigate_to_tile', args=[next_tile]))
    
    # Marcar el tile como ocupado
    occupy_tile(tile)
    coords = find_by_filter({'tile': tile})
    num_penguins = count_total()
    print(coords)
    return render(request, 'count_penguins.html', {
        'tile': tile,
        'number' : number,
        'coords': coords,
        'count': num_penguins
        })


def increment_tile(request, current_tile):
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

    print("TILE ACTUAL QUE VAMOS A INCREMENTAR: ", current_tile)
    prefix, number = current_tile.rsplit('_', 1)
    next_number = int(number) + 1
    contador = 0
    request.session['all_penguins_done'] = False
    while True:
        if next_number > 500:
            request.session['all_penguins_done'] = True
            return redirect(f'/')

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


