
from django.conf import settings
import os
import csv
#import rasterio
import pandas as pd



# Function to get bounds of a TIFF file
def get_image_bounds(tiff_path:str) -> tuple:
    """
    Devuelve la esquina superior izquierda y la esquina inferior derecha de la imagen seleccionada.
    La función transform*(0,0) se encarga de devolver el sistema georeferneciasa del archivo (NO en píxeles).

    Args:
    - tiff_path: str, ruta completa del archivo TIFF.
    """
    with rasterio.open(tiff_path) as src:
        transform = src.transform
        width, height = src.width, src.height

        # Upper-left corner
        ul_x, ul_y = transform * (0, 0)
        # Bottom-right corner
        br_x, br_y = transform * (width, height)
        return ul_x, ul_y, br_x, br_y


# Función para convertir píxeles a coordenadas geográficas
def pixel_to_coordinates(
    tile_name:str, 
    pixel_x:int, 
    pixel_y:int, 
    csv_corners_data: str = os.path.join(settings.BASE_DIR, 'static', 'data', 'ortho_coordinates.csv'),
    path_tiff_files: str = os.path.join(settings.BASE_DIR, 'static', 'img')
):
    """
    Esta función está pensada para llamarse dentro de un bucle for donde se itere 
    sobre el JSON con todos los tiles con los píxeles marcados.

    Convierte las coordenadas del píxel (pixel_x, pixel_y) de una imagen (tile) a coordenadas geográficas
    usando la información de los límites geográficos (upper_left, bottom_right) que se encuentra en el CSV.
    
    Args:
    - tile_name (str): Nombre de la imagen/fragmento del ortomosaico.
    - pixel_x (int): Posición X del píxel marcado en la imagen.
    - pixel_y (int): Posición Y del píxel marcado en la imagen.
    - csv_corners_data (str): Ruta al archivo CSV con las coordenadas de las esquinas de las imágenes.
    - path_img_files: path a donde se encuentran las imágenes para medir su ancho y alto.
    
    Returns:
    - tuple: Coordenadas geográficas (x, y).
    """
    df_corners = pd.read_csv(csv_corners_data)

    # Verificar si el tile_name está en el DataFrame
    if tile_name not in df_corners['file'].values:
        raise ValueError(f"El tile '{tile_name}' no se encuentra en el archivo CSV.")

    # Obtener la fila correspondiente al tile
    tile_row = df_corners[df_corners['file'] == tile_name].iloc[0]
    x_top, y_top = tile_row['x_top'], tile_row['y_top']
    x_bot, y_bot = tile_row['x_bot'], tile_row['y_bot']

    # Construir la ruta al archivo TIFF
    tiff_path = os.path.join(path_tiff_files, f"{tile_name}.tif")

    # Obtener el ancho y alto de la imagen usando rasterio
    with rasterio.open(tiff_path) as src:
        width, height = src.width, src.height
    print(f"Ancho de la imagen: {width} píxeles. Alto de la imagen: {height} píxeles")

    # Calcular las proporciones de las coordenadas geográficas
    x_ratio = pixel_x / width
    y_ratio = pixel_y / height

    # Calcular las coordenadas geográficas usando las proporciones
    geo_x = x_top + x_ratio * (x_bot - x_top)
    geo_y = y_top + y_ratio * (y_bot - y_top)

    return geo_x, geo_y