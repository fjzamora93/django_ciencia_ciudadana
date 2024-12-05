Arrancar el servidor:
```bash
myenv\Scripts\activate

cd cienciaciudadana
python manage.py runserver
```


# Servir archivos estáticos -cada vez que cambias la carpeta de static
```bash
python manage.py collectstatic
```


1. Crear un entorno virtual y activarlo

```bash
python3 -m venv myenv


# DESDE LA CARPETA RAÍZ DEL PROYECTO, ACTIVAR DIRECTAMENTE ASÍ:
myenv\Scripts\activate
```

2. Crear el proyecto de Django

```bash
django-admin startproject myproject
```

3. Crear una aplicación

```bash
cd myproject
python manage.py startapp myapp
```


Ahora nos vamos al archivo principal desettings.py y haremos lo siguiente:
1. Registraremos cada aplicación que vayamos a crear.
2. Añadimos la URL del host que vayamos a utilizar en ALLOWED_HOSTS.

```python
ALLOWED_HOSTS = [
    'http://127.0.0.1:8000/', 
]

INSTALLED_APPS = [
    ...
    'myapp',
]
```



Crear una vista para "Hola Mundo": Abre nueva_app/views.py y añade la siguiente vista:

```python
from django.http import HttpResponse

def hola_mundo(request):
    return HttpResponse("Hola Mundo")
```


Configurar las rutas (URLs): Crea un archivo urls.py dentro de la carpeta hola y añade lo siguiente:

```python
from django.urls import path
from .views import hola_mundo

urlpatterns = [
    path('', hola_mundo, name='hola_mundo'),
]
```

Incluir las rutas de la aplicación en el proyecto principal: Abre cienciaciudana/urls.py y modifica el archivo para incluir las rutas de la aplicación hola:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
]
```

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

- Añadimos dentro settings.py la ruta de la carpeta templates en el DIR.

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