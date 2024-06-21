# main_page/views.py
from django.shortcuts import render
from django.http import HttpResponse  # или другие необходимые классы

def index(request):
    return render(request, 'main-page/index.html')
