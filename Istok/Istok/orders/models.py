from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from catalog.models import Product
from users.models import User, LoyaltyProgram


class Order(models.Model):
    """
    Модель заказа.
    """
    STATUS_CHOICES = [
        ('Processing', _('В обработке')),
        ('Awaiting payment', _('Ожидает оплаты')),
        ('Awaiting measurement', _('Ожидание технического замера')),
        ('Correction measurement', _('Корректировка после технического замера')),
        ('Preparation a sketch', _('Подготовка эскиза')),
        ('Processing construction', _('Обработка конструктором')),
        ('Production', _('Производство')),
        ('Preparation for delivering', _('Подготовка к доставке')),
        ('Delivered', _('Доставляется')),
        ('Montage', _('Монтаж')),
        ('Returned', _('Возврат')),
        ('Completed', _('Завершен')),
        ('Cancelled', _('Отменен')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    order_number = models.AutoField(primary_key=True, verbose_name=_('Номер заказа'))
    address = models.CharField(max_length=255, verbose_name=_('Адрес доставки'))
    phone_number = PhoneNumberField(verbose_name=_('Номер телефона для связи'))
    comment = models.TextField(null=True, blank=True, verbose_name=_('Комментарий к заказу'))
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Стоимость доставки'))
    installation_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Стоимость установки'))
    used_points = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Использованные баллы'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Общая стоимость заказа'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания заказа'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', verbose_name=_('Статус заказа'))

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def cost_calculation(self):
        """
        Рассчитывает общую стоимость заказа, включая стоимость продуктов, доставки и установки.
        """
        total_product_price = sum(order_product.product_price for order_product in self.orderproduct_set.all())
        total_price = self.delivery_cost + self.installation_cost + total_product_price

        # Валидация используемых баллов
        if self.used_points < 0:
            raise ValueError(_('Использованные баллы не могут быть отрицательными'))
        if self.used_points > total_price:
            raise ValueError(_('Использованные баллы не могут быть больше общей стоимости заказа'))

        # Проверка баланса пользователя
        user_loyalty_program = LoyaltyProgram.objects.get(user=self.user)
        if user_loyalty_program.balance < self.used_points:
            raise ValueError(_('Недостаточно баллов для выполнения заказа'))

        # Учитываем использованные баллы
        total_price -= self.used_points

        # Убедиться, что стоимость не отрицательная
        if total_price < 0:
            raise ValueError(_('Общая стоимость заказа не может быть отрицательной'))

        return total_price

    def save(self, *args, **kwargs):
        # Проверяем, есть ли уже первичный ключ (заказ уже существует в базе данных)
        if self.pk:
            # Получаем старую версию заказа
            old_order = Order.objects.get(pk=self.pk)

            # Проверяем изменение статуса заказа
            if old_order.status != self.status:
                # Если статус изменился, создаем новую запись в истории статусов
                OrderStatusHistory.objects.create(order=self, status=self.status)

            # Вычисляем разницу в использованных баллах
            points_difference = self.used_points - old_order.used_points

            # Обновляем баланс пользователя с учетом изменений в использованных баллах
            user_loyalty_program = LoyaltyProgram.objects.get(user=self.user)
            user_loyalty_program.balance -= points_difference
            user_loyalty_program.save()
        else:
            # Если заказ только создается, создаем запись в истории статусов
            super().save(*args, **kwargs)
            OrderStatusHistory.objects.create(order=self, status=self.status)

            # Вычитаем использованные баллы из баланса пользователя
            user_loyalty_program = LoyaltyProgram.objects.get(user=self.user)
            user_loyalty_program.balance -= self.used_points
            user_loyalty_program.save()

        # Перед сохранением рассчитываем общую стоимость
        self.total_price = self.cost_calculation()

        # Сохраняем объект
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заказ {self.order_number} - {self.user}'


class OrderProduct(models.Model):
    """
    Модель продуктов в заказе.

    Данная модель нужна, чтобы цена в истории заказов не изменялась, если цену продукта изменят в будущем.
    К тому же это позволяет более гибко устанавливать цену продукта в конкретном заказе,
    не привязываясь к цене в каталоге.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Заказ'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Продукт'))
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена продукта'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Количество'))

    class Meta:
        verbose_name = _('Продукт в заказе')
        verbose_name_plural = _('Продукты заказа')

    def __str__(self):
        return f'{self.product} в заказе {self.order}'


class OrderStatusHistory(models.Model):
    """
    Модель для хранения истории статусов заказа.
    """
    STATUS_CHOICES = Order.STATUS_CHOICES

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name=_('Заказ'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing', verbose_name=_('Статус заказа'))
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата изменения'))

    class Meta:
        verbose_name = _('История статусов заказа')
        verbose_name_plural = _('Истории статусов заказов')

    def __str__(self):
        return f"{self.order} - {self.status} at {self.changed_at}"
