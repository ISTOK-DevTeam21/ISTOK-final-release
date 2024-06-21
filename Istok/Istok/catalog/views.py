from django.shortcuts import render
from django.views.generic import View
from .models import Product, Promotion


def product_promotion(request):
    """
     Представление для показа списков активных акций и списков активных продуктов
    """
    if request.method == "GET":
        products = Product.objects.filter(is_catalog=True).order_by('-created_at')
        promotions = Promotion.objects.filter(is_active=True).order_by('-start_date')
        product_type = request.GET.get('type')
        if product_type:
            products = Product.objects.filter(is_catalog=True, categories__name=product_type).order_by('-created_at')
        context = {
            'products': products,
            'promotions': promotions,
        }
        return render(request, 'catalog/product_promotion_list.html', context=context)
