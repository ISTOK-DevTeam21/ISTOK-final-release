# about_is/views.py
from django.shortcuts import render
from django.http import HttpResponse  # или другие необходимые классы


def about_us(request):
    return render(request, 'main-page/about.html')

