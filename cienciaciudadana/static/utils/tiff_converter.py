from PIL import Image
import os

# Ruta de entrada y salida
input_folder = "../img/sample/train" 
output_folder = "../img/"  

# Asegúrate de que la carpeta de salida existe
os.makedirs(output_folder, exist_ok=True)

# Convertir todos los archivos TIFF a PNG
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith(".tiff"):  
        tiff_path = os.path.join(input_folder, file_name)
        png_path = os.path.join(output_folder, file_name.replace(".tiff", ".jpg"))

        # Abrir y convertir la imagen
        with Image.open(tiff_path) as img:
            rgb_img = img.convert("RGB")
            rgb_img.save(png_path, "JPEG")
            print(f"Convertido: {file_name} -> {png_path}")

print("¡Conversión completa!")