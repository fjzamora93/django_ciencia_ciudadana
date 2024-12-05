## Arrancar el servidor (cada vez que queramos iniciarlo)

Antes de arrancar el proyecto, activamos el entorno virtual. Debemos activar el entorno virtual desde la carpeta en la que esté myenv.

```bash
cd rutaProyecto
myenv\Scripts\activate
python manage.py runserver
```

## Servir archivos estáticos - opcional

Cada vez que cambias la carpeta de static, y únicamente si vas a servir los archivos estáticos desde otro lugar, es necesario hacer la recolección. 
```bash
python manage.py collectstatic
```

# Crewación de un proyecto nuevo

crear proyecto > crear aplicacion > añadir hosts a settings > añadir hosts permitidos > crear vista > configurar rutas > realizar migraciones > añadir templates en settings

## 1. Crear un entorno virtual y activarlo

```bash
python3 -m venv myenv


# DESDE LA CARPETA RAÍZ DEL PROYECTO, ACTIVAR DIRECTAMENTE ASÍ:
myenv\Scripts\activate
```

## 2. Crear el proyecto de Django

```bash
django-admin startproject myproject
```

## 3. Crear una aplicación

```bash
cd myproject
python manage.py startapp myapp
```

## 4. Añadimos los host permitidos y las aplicaciones instaladas

Ahora nos vamos al archivo principal de settings.py y haremos lo siguiente:
1. Registraremos cada aplicación que vayamos a crear.
2. Añadimos la URL del host que vayamos a utilizar en ALLOWED_HOSTS.

```python

INSTALLED_APPS = [
    ...
    'myapp',
]

# Allowed hosts no incluye el https
ALLOWED_HOSTS = [
    'cienciaciudadana-pinguinos.up.railway.app',
    '127.0.0.1',
    'localhost',

]

# El csrf debe incluir el http o el https
CSRF_TRUSTED_ORIGINS = [
    'https://cienciaciudadana-pinguinos.up.railway.app',
    'http://127.0.0.1',
]


```

## 5. Crear una vista

Crear una vista para "Hola Mundo": Abre nueva_app/views.py y añade la siguiente vista:

```python
from django.http import HttpResponse

def hola_mundo(request):
    return HttpResponse("Hola Mundo")
```

## 6. Configurar las rutas

Configurar las rutas (URLs): Crea un archivo urls.py dentro de la carpeta hola y añade lo siguiente:

```python
from django.urls import path
from .views import hola_mundo

urlpatterns = [
    path('', hola_mundo, name='hola_mundo'),
]
```

## 7. Incluir las rutas de la aplicación en el proyecto principal

Incluir las rutas de la aplicación en el proyecto principal: Abre cienciaciudana/urls.py y modifica el archivo para incluir las rutas de la aplicación hola:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
]
```

## 8. Realizar las migraciones

Si seguimos estos pasos podremos correr el servidor, aunque nos dará el error de las migraciones. Asi que aplicaremos las migraciones.

```bash
python manage.py migrate
python manage.py runserver
```



## Estructura de la app

```bash	
myApp/
├── templates/
│   └── hola/
│       └── hola_mundo.html
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```


## 9. Incluir las templates en settings

Añadimos dentro settings.py la ruta de la carpeta templates en el DIR.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myApp','templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```


## 10. Configurar las variables de entorno

Instala python-decouple para manejar las variables de entorno.

```bash
pip install python-decouple
```

En un documento llamado .env, dentro de la raíz del proyecto, añade las variables de entorno.

```bash
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```


Ahora, cuando quieras usar las variables de entorno en cualquier parte del proyecto, solamente tendrás que importar la librería y llamar a la variable.

```python
import environ

# CARGAR VARIABLES DE ENTORNO
env = environ.Env()
environ.Env.read_env()

# URL de conexión con tu MongoDB Atlas
MONGO_URI = env('MONGO_URI')
```