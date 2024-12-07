from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('save-coords/', views.save_coords, name='save_coords'),
    path('find-tile/', views.find_tile, name='find_tile'),
    path(f'<str:tile>/', views.navigate_to_tile, name='navigate_to_tile'),
]

