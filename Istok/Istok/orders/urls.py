from django.urls import path
from .views import current_orders, order_history, order_detail

urlpatterns = [
    path('current-orders/', current_orders, name='current_orders'),
    path('order-history/', order_history, name='order_history'),
    path('order/<int:pk>/', order_detail, name='order_detail'),
]
