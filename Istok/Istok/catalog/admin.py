from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, Promotion, PromotionImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Category.

    List display: Отображение списка категорий.
    Search fields: Поиск категорий по имени.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Product.

    List display: Отображение списка продуктов.
    Search fields: Поиск продуктов по имени.
    """
    list_display = ('name', 'price', 'is_active', 'is_catalog', 'display_categories', 'sketchfab_embed_display')
    search_fields = ('name',)

    def sketchfab_embed_display(self, obj):
        return format_html(obj.sketchfab_embed)

    def display_categories(self, obj):
        """
            Отображение категорий продукта в админ-панели.
            """
        return ', '.join([category.name for category in obj.categories.all()])

    display_categories.short_description = 'Категории'
    sketchfab_embed_display.short_description = 'Код для встраивания Sketchfab'
    sketchfab_embed_display.allow_tags = True


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Административная панель для модели ProductImage.

    List display: Отображение списка изображений продуктов.
    """
    list_display = ('product', 'image')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Promotion.

    List display: Отображение списка акций.
    Search fields: Поиск акций по имени.
    """
    list_display = ('name', 'description', 'is_active', 'start_date', 'end_date')
    search_fields = ('name',)


@admin.register(PromotionImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Административная панель для модели ProductImage.

    List display: Отображение списка изображений продуктов.
    """
    list_display = ('promotion', 'image')
