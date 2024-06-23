from django.urls import path
from .views import current_orders, order_history, order_detail

urlpatterns = [
    path('current-orders/', current_orders, name='current_orders'),
    path('orders-history/', order_history, name='order_history'),
    path('orders/<int:pk>/', order_detail, name='order_detail'),
]
