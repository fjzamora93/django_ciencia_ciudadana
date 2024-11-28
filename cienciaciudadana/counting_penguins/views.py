from django.shortcuts import render

from django.http import HttpResponse


def hola_mundo(request):
     return render(request, 'index.html')