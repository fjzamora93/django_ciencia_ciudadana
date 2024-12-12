# Extracción de coordenadas de los tiles (pensado para hacer desde google drive con colab)

import os
import csv
import rasterio
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
        return (ul_x, ul_y), (br_x, br_y)

# Path to your TIFF files
input_path = os.path.join('G:', '.shortcut-targets-by-id', '1pYgV5EIk4-LapLNhlCwpQaDAzuqNffXG', 'doctorado_albert', 'Pinguiton', 'ortho_enero_500')
tiff_files = [file for file in os.listdir(input_path) if file.endswith(('.tif', '.TIF'))]

# CSV output file
output_csv = "../data/ortho_coordinates.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Writing to CSV
with open(output_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["file", "upper_left", "bottom_right"])

    # Process and write all TIFF files
    for file_name in tiff_files:
        tiff_path = os.path.join(input_path, file_name)  
        upper_left, bottom_right = get_image_bounds(tiff_path)
        writer.writerow([file_name, upper_left, bottom_right])

print(f"CSV file '{output_csv}' has been created.")