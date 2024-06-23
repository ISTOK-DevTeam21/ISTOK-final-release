from django import template

register = template.Library()

@register.filter()
def get_img(product_object, value):
    if product_object.images.exists() and len(product_object.images.all()) > value:
        image_path = product_object.images.all()[value].image.url  # Assuming 'image' is an ImageField
        return image_path
    return ''
