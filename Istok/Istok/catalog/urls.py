from django.urls import path
from .views import product_catalog, direct_kitchens


urlpatterns = [
    path('', product_catalog, name='prod-catalog'),
    path('kitchens/direct', direct_kitchens, name='direct-kitchens')

]
