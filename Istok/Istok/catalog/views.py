from django.shortcuts import render
from django.views.generic import View
from .models import Product, Promotion


def product_catalog(request):
    return render(request, 'main-page/catalog.html')


def corner_kitchens(request):
    """
    Представление для показа угловых кухонь
    """
    if request.method == "GET":
        kitchens = Product.objects.filter(is_catalog=True, categories__name='Прямые кухни').order_by('-created_at')
        context = {
            'kitchens': kitchens
        }
        return render(request, 'main-page/kitchen.html', context=context)
