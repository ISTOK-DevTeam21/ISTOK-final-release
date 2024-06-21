from django.contrib import admin
from .models import Order, OrderProduct, OrderStatusHistory


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'changed_at')
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'date', 'status', 'total_price')
    list_filter = ('status', 'date')
    search_fields = ('order_number', 'user__phone_number', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('-date', 'user__last_name', 'user__first_name', 'user__phone_number')
    inlines = [OrderProductInline, OrderStatusHistoryInline]

    def __str__(self):
        return f'Заказ {self.order_number} - {self.user}'


class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'changed_at')
    list_filter = ('status', 'changed_at')
    search_fields = ('order__order_number', 'order__user__phone_number', 'order__user__email', 'order__user__first_name', 'order__user__last_name')
    ordering = ('-changed_at', 'order__order_number')

    def __str__(self):
        return f'{self.order} - {self.status} at {self.changed_at}'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatusHistory, OrderStatusHistoryAdmin)
