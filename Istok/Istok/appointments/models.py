from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Status(models.Model):
    """
    Модель для статусов встреч
    """
    STATUS_APPOINTMENTS_CHOICES = [
        ('not_commited', _('Не совершена')),
        ('commited', _('Совершена'))
    ]
    status_name = models.CharField(max_length=255,
                                   choices=STATUS_APPOINTMENTS_CHOICES,
                                   unique=True,
                                   default='not_commited',
                                   verbose_name=_('Название статуса встречи')
                                   )

    class Meta:
        verbose_name = _('Статус')
        verbose_name_plural = _('Статусы')

    def __str__(self):
        return self.get_status_name_display()


class Appointment(models.Model):
    """
    Модель встреч для пользователей
    """
    staff_user = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   related_name='staff_appointments',
                                   verbose_name=_('Пользователь персонала')
                                   )
    client_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    related_name='client_appointments',
                                    verbose_name=_('Пользователь клиента')
                                    )
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name=_('Статус встречи'))
    date = models.DateField(verbose_name=_('Дата встречи'))
    time = models.TimeField(verbose_name=_('Время встречи'))
    is_booked = models.BooleanField(default=True, verbose_name=_('Забронирована ли встреча'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Время создания встречи'))

    def __str__(self):
        return f'{self.date} {self.time} - {self.staff_user} with {self.client_user} | {self.status}'

    class Meta:
        verbose_name = _('Встреча')
        verbose_name_plural = _('Встречи')
