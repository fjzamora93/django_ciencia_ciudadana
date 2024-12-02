from PIL import Image
import os

# Ruta de entrada y salida
input_folder = "../img/sample/train" 
output_folder = "../img/"  

# Asegúrate de que la carpeta de salida existe
os.makedirs(output_folder, exist_ok=True)

# Convertir todos los archivos TIFF a PNG
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(".tiff"):  # Verificar que el archivo sea TIFF
        tiff_path = os.path.join(input_folder, file_name)
        png_path = os.path.join(output_folder, file_name.replace(".tiff", ".png"))

        # Abrir y convertir la imagen
        with Image.open(tiff_path) as img:
            img.save(png_path, "PNG")
            print(f"Convertido: {file_name} -> {png_path}")

print("¡Conversión completa!")