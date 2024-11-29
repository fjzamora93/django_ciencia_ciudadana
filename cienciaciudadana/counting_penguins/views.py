from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import os
import pandas as pd

def hola_mundo(request):
     return render(request, 'index.html')



def save_coords(request):
    if request.method == 'POST':
        try:
            coords_list = json.loads(request.POST.get('coords', '[]'))
            df = pd.DataFrame(coords_list)
            file_path = os.path.join('static', 'data', 'coords.json')
            
            df.to_json(file_path, orient='records', indent=2)
            
            return JsonResponse({'message': f'Coordinates saved successfully  {df}'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'message': 'Invalid request'}, status=400)


# def save_coords(request):
#     if request.method == 'POST':
#         try:
#             coords_list = json.loads(request.POST.get('coords', '[]'))
#             file_path = os.path.join('static', 'data', 'coords.json')
            
#             with open(file_path, 'w') as json_file:
#                 json.dump(coords_list, json_file, indent=2)
            
#             return JsonResponse({'message': 'Coordinates saved successfully'})
#         except json.JSONDecodeError:
#             return JsonResponse({'message': 'Invalid JSON data'}, status=400)
#     return JsonResponse({'message': 'Invalid request'}, status=400)