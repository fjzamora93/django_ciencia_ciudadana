
Para empaquetar tu proyecto Django en un contenedor Docker y desplegarlo en Railway, sigue estos pasos detallados:

# IMPORTANTE.

Después de cada cambio, hay que reconstruir siempre la imagen (solamente para desplegar el Docker, no hace falta si es sobre github)

```bash

# por ejemplo:
docker build -t pinguiton .
docker push fjzamora93/pinguiton:latest

```


# 1. Configura tu proyecto Django
Asegúrate de que tu proyecto está listo para producción:

Revisa que los archivos estáticos estén configurados.
Define correctamente las variables de entorno en tu aplicación.

```python
# settings.py
DEBUG = True # Lo recomendable es cambiarlo a False en producción, pero puede ser útil para detectar errores en el despliegue.
ALLOWED_HOSTS = ['*']  
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

# 2. Recopilación de estáticos (opcional)

Si vas a servir los archivos estáticos directametne desde el propio proyecto de github, es mejor no hacer la recolección.

Sin embargo, si optas por servirlos desde otro lugar, será necesario hacer la recopilación. En este caso no es necesario.

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
Después de realizar todas las instalaciones en tu entorno virtual, puedes generar el archivo de requirements.

```bash
pip freeze > requirements.txt
```


# 5. Abrir Docker Desktop. Construye y prueba tu imagen Docker

Construye tu imagen Docker y pruébala localmente antes de desplegarla en Railway.
Para ello, será necesario tener abierto DockerDescktop.

### Opcional -> subir el proyecto a DockerHub
En tu caso, los repositorios de dockerhub son estos:
-fjzamora93/pinguiton:latest
-fjzamora93/tu-imagen:latest

```bash
docker login
docker build -t nombre_imagen .

# por ejemplo:
docker build -t nombre_imagen .
docker push fjzamora93/nombre_imagen:latest

docker run --env-file .env -p 8000:8000 django-app
```

Si navegas hasta http://127.0.0.1:8000 deberías ver tu aplicación Django funcionando.

## Posibles errores

Es posible que no esté funcionando, para ello vamos a ver qué imágenes tenemos en Docker:

```bash
docker ps


# Deberías ver en pantalla algo como esto:*
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                    NAMES       
0e7b644aaac8   django-app   "gunicorn --bind 0.0…"   57 seconds ago   Up 56 seconds   0.0.0.0:8000->8000/tcp   loving_tesla
```

Si no aparece esto, quiere decir que algo salió mal. Posiblemente haya algún propelma relacionado con las variables e entorno.

## Inspeccionar las variables del entorno. 

Es posibe inspeccionar que las variables del entorno están correctamente cargadas así:

```bash
docker exec -it loving_tesla /bin/sh
env
```

# 6. Despliega tu aplicación en Railway

Una vez que tu aplicación funciona localmente, despliégala en Railway desde el github. En total, debes asegurarte que dispones de los siguientes archivos en tu repositorio:

```bash	
raiz_proyecto/
├── .env
├── .dockerignore
├── Dockerfile
├── requirements.txt
├── manage.py
├── cienciaciudadana/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── __init__.py
├── myapp/
├── El resto de tus aplicaciones

```
