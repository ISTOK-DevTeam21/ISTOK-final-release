# main_page/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main_page_index'),
    # Другие маршруты вашего приложения main_page, если они будут
]