
Para empaquetar tu proyecto Django en un contenedor Docker y desplegarlo en Railway, sigue estos pasos detallados:

# 1. Configura tu proyecto Django
Asegúrate de que tu proyecto está listo para producción:

Revisa que los archivos estáticos estén configurados.
Define correctamente las variables de entorno en tu aplicación.

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['*']  # Cambia según tus necesidades
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

# 2. Recopilación de estáticos

```bash
python manage.py collectstatic --noinput
```

# 3. Crea un archivo Dockerfile

Este archivo define cómo empaquetar tu aplicación Django en un contenedor Docker. Colócalo en la raíz del proyecto.

```Dockerfile
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
```


# 3. Crear un .dockerignore en la raíz del proyecto

```
*.pyc
__pycache__/
.env
myenv/
.git
```

# 4. Crea un archivo requirements.txt

Crear un archivo requirements.txt en la raíz del proyecto con las dependencias necesarias para tu aplicación Django.




# 5. Abrir Docker Desktop. Construye y prueba tu imagen Docker

Construye tu imagen Docker y pruébala localmente antes de desplegarla en Railway.
 Para ello, será necesario tener abierto DockerDescktop.

```bash
docker build -t django-app .
docker run --env-file .env -p 8000:8000 django-app
```

En caso de error, podemos añadir el MONGO_URI como un parámetro:


```bash
docker ps
```

*Deberías ver en pantalla algo como esto:*

```bash
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                    NAMES       
0e7b644aaac8   django-app   "gunicorn --bind 0.0…"   57 seconds ago   Up 56 seconds   0.0.0.0:8000->8000/tcp   loving_tesla
```

## Inspeccionar las variables del entorno. 

Es posibe inspeccionar que las variables del entorno están correctamente cargadas así:

```bash
docker exec -it loving_tesla /bin/sh
env
```