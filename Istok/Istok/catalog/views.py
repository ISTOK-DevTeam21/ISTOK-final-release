from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from .models import Product, Promotion


def product_catalog(request):
    return render(request, 'main-page/catalog.html')



def direct_kitchens(request):
    """
    View to display direct kitchens with optional filtering.
    """
    # Fetch all products initially
    kitchens = Product.objects.filter(is_catalog=True, categories__name='Прямые кухни').order_by('-created_at')

    # Get filter parameters from GET request
    kitchen_material_facade = request.GET.getlist('material_facade')
    kitchen_material_table_top = request.GET.getlist('material_table_top')
    kitchen_material_apron = request.GET.getlist('material_apron')
    kitchen_styles = request.GET.getlist('style')

    # Initialize Q object to build the filter conditions
    filters = Q()

    # Apply filters only if they are selected
    if kitchen_material_facade:
        filters &= Q(material_facade__in=kitchen_material_facade)
    if kitchen_material_table_top:
        filters &= Q(material_table_top__in=kitchen_material_table_top)
    if kitchen_material_apron:
        filters &= Q(material_apron__in=kitchen_material_apron)
    if kitchen_styles:
        filters &= Q(style__in=kitchen_styles)

    # Filter kitchens based on the constructed filters
    if filters:
        kitchens = kitchens.filter(filters)
    else:
        # If no filters selected, display all kitchens
        kitchens = kitchens.all()

    context = {
        'kitchens': kitchens
    }
    return render(request, 'main-page/kitchen.html', context=context)