from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_page.urls')),  # добавляем пустой путь для main_page
    path('', include('orders.urls')),
    path('appointments/', include('appointments.urls')),
    path('catalog/', include('catalog.urls')),
    path('about/', include('about_us.urls')),
    path('accounts/', include('accounts.urls')),
]


