from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from .models import Product, Promotion


def product_catalog(request):
    return render(request, 'main-page/catalog.html')


def direct_kitchens(request):
    """
    Представление для показа угловых кухонь
    """
    if request.method == "GET":
        kitchens = Product.objects.filter(is_catalog=True, categories__name='Прямые кухни').order_by('-created_at')

        kitchen_material_facade = request.GET.getlist('material_facade', [])
        kitchen_material_table_top = request.GET.getlist('material_table_top', [])
        kitchen_material_apron = request.GET.getlist('material_apron', [])
        kitchen_category_styles = request.GET.getlist('style', [])

        if kitchen_material_facade or kitchen_material_table_top or kitchen_material_apron or kitchen_category_styles:
            kitchens = Product.objects.filter(
                (Q(is_catalog=True) &
                 Q(categories__name='Прямые кухни')) &
                Q(material_facade__in=kitchen_material_facade) |
                Q(material_table_top__in=kitchen_material_table_top) |
                Q(material_apron__in=kitchen_material_apron)
            ).order_by('-created_at')
        context = {
            'kitchens': kitchens
        }
        return render(request, 'main-page/kitchen.html', context=context)
