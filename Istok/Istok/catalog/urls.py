from django.urls import path
from .views import product_catalog, corner_kitchens


urlpatterns = [
    path('', product_catalog, name='prod-catalog'),
    path('kitchens/direct', corner_kitchens, name='direct-kitchens')

]
