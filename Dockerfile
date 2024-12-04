# Usa una imagen base de Python
FROM python:3.10-slim

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el archivo .env y el resto de los archivos del proyecto
COPY . .

# Instala dotenv para cargar variables de entorno desde el archivo .env
RUN pip install python-dotenv

# Carga las variables de entorno desde el archivo .env y ejecuta collectstatic en el mismo comando
RUN python -c "import os; from dotenv import load_dotenv; load_dotenv('.env'); os.system('python manage.py collectstatic --noinput')"

# Expone el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cienciaciudadana.wsgi"]