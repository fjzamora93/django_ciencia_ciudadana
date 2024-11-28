from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hola_mundo, name='hola_mundo'),
]