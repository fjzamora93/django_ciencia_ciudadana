# Extracción de coordenadas de los tiles (pensado para hacer desde google drive con colab)

import os
import csv
import rasterio


# Function to get bounds of a TIFF file
def get_image_bounds(tiff_path):
    with rasterio.open(tiff_path) as src:
        transform = src.transform
        width, height = src.width, src.height
        # Upper-left corner
        ul_x, ul_y = transform * (0, 0)
        # Bottom-right corner
        br_x, br_y = transform * (width, height)
        return (ul_x, ul_y), (br_x, br_y)

# Path to your TIFF files
input_path = '/content/drive/My Drive/doctorado_albert/Pinguiton/ortho_enero_500'
tiff_files = [file for file in os.listdir(input_path) if file.endswith(('.tif', '.TIF'))]

# CSV output file
output_csv = "ortho_coordinates.csv"


# Path to your TIFF files
input_path = '/content/drive/My Drive/doctorado_albert/Pinguiton/ortho_enero_500'
tiff_files = [file for file in os.listdir(input_path) if file.endswith(('.tif', '.TIF'))]

# CSV output file
output_csv = "ortho_coordinates.csv"


# Path to your TIFF files
input_path = '/content/drive/My Drive/doctorado_albert/Pinguiton/ortho_enero_500'
tiff_files = [file for file in os.listdir(input_path) if file.endswith(('.tif', '.TIF'))]

# CSV output file
output_csv = "ortho_coordinates.csv"