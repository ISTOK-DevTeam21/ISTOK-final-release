from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def current_orders(request):
    """
    Представление для отображения текущих заказов пользователя.
    """
    user = request.user
    orders = Order.objects.filter(user=user).exclude(status__in=['Completed', 'Cancelled', 'Returned'])
    return render(request, 'orders/current_orders.html', {'orders': orders})

@login_required
def order_history(request):
    """
    Представление для отображения истории заказов пользователя.
    """
    user = request.user
    orders = Order.objects.filter(user=user, status__in=['Completed', 'Cancelled', 'Returned'])
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    """
    Представление для отображения деталей заказа и истории его статусов.
    """
    order = get_object_or_404(Order, pk=pk)
    status_history = order.status_history.all()
    return render(request, 'orders/order_detail.html', {'order': order, 'status_history': status_history})
