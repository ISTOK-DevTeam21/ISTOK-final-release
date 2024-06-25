# about_us/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.about_us, name='about-us'),
    path('contacts/', views.where_we_are, name='where-we-are'),
    # Другие маршруты вашего приложения main_page, если они будут
]
