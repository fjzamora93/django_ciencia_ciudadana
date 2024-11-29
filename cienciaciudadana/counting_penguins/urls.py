from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hola_mundo, name='hola_mundo'),
    path('save-coords/', views.save_coords, name='save_coords'),
]