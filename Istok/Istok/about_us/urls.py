# about_us/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.about_us, name='about-us'),
    # Другие маршруты вашего приложения main_page, если они будут
]
