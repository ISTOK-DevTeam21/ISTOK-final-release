from django.urls import path
from .views import product_promotion


urlpatterns = [
    path('', product_promotion, name='prod-catalog')
]
