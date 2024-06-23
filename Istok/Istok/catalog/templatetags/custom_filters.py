from django import template


register = template.Library()


@register.filter()
def get_img(product_object, value):
    return product_object.images.all()[value].image
