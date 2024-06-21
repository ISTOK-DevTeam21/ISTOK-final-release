import string

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User без поля username.
    Предоставляет методы для создания обычных пользователей и суперпользователей.
    """

    def create_user(self, email, phone_number, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с заданными email, номером телефона и паролем.
        """
        if not phone_number:
            raise ValueError(_('Поле номера телефона должно быть заполнено.'))

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с заданными email, номером телефона и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя, использующая номер телефона вместо имени пользователя.
    """
    REPAIR_DATE_CHOICES = [
        ('ongoing', _('Уже идет')),
        ('soon', _('Скоро приступаем')),
        ('six_months', _('В течение полугода')),
        ('one_year', _('В течение года')),
    ]

    email = models.EmailField(null=True, blank=True, unique=True, verbose_name=_('Электронная почта'))
    first_name = models.CharField(max_length=150, verbose_name=_('Имя'))
    last_name = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Фамилия'))
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Отчество'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Дата рождения'))
    phone_number = PhoneNumberField(unique=True, verbose_name=_('Номер телефона'))
    phone_is_confirmed = models.BooleanField(_('Телефон подтвержден'), default=False)
    has_children = models.BooleanField(default=False, verbose_name=_('Наличие детей'))
    repair_planned = models.BooleanField(default=False, verbose_name=_('Планируется ли ремонт'))
    repair_date = models.CharField(
        max_length=255,
        choices=REPAIR_DATE_CHOICES,
        null=True,
        blank=True,
        verbose_name=_('Когда планируется ремонт')
    )
    repair_rooms = models.ManyToManyField(
        'Room',
        blank=True,
        verbose_name=_('Комнаты, в которых планируется ремонт')
    )
    subscribe_newsletter = models.BooleanField(default=True, verbose_name=_('Согласие на рассылку'))
    consent_personal_data = models.BooleanField(
        default=True,
        verbose_name=_('Согласие на обработку персональных данных')
    )

    is_staff = models.BooleanField(default=False, verbose_name=_('Является сотрудником'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))
    date_joined = models.DateTimeField(_("Дата регистрации"), default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Room(models.Model):
    """
    Модель для хранения типов помещений.
    """
    REPAIR_ROOMS_CHOICES = [
        ('kitchen', 'Кухня'),
        ('hallway', 'Коридор'),
        ('entryway', 'Прихожая'),
        ('bathroom', 'Ванная'),
        ('children', 'Детская'),
        ('bedroom', 'Спальня'),
        ('living_room', 'Гостиная'),
        ('dining_room', 'Столовая'),
        ('office', 'Кабинет')
    ]
    name = models.CharField(max_length=255, choices=REPAIR_ROOMS_CHOICES, verbose_name=_('Название'))

    class Meta:
        verbose_name = _('Тип помещения')
        verbose_name_plural = _('Типы помещений')

    def __str__(self):
        for key, value in self.REPAIR_ROOMS_CHOICES:
            if key == self.name:
                return value
        return self.name


class LoyaltyProgram(models.Model):
    """
    Модель программы лояльности для пользователей.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    balance = models.IntegerField(default=0, verbose_name=_('Баланс'))
    referral_code = models.CharField(max_length=255, unique=True, verbose_name=_('Реферальный код'))

    class Meta:
        verbose_name = _('Программа лояльности')
        verbose_name_plural = _('Программы лояльности')

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_unique_referral_code()

        if self.pk:
            # Получаем старое значение баланса из базы данных
            old_balance = LoyaltyProgram.objects.get(pk=self.pk).balance
            if self.balance != old_balance:
                # Разница между новым и старым балансом
                points_delta = self.balance - old_balance
                # Создаем запись в LoyaltyTransaction
                LoyaltyTransaction.objects.create(
                    user=self.user,
                    points=points_delta,
                )
        else:
            self.balance = 0

        super().save(*args, **kwargs)

    def generate_referral_code(self, length=8):
        characters = string.ascii_uppercase + string.digits
        return get_random_string(length, characters)

    def generate_unique_referral_code(self):
        referral_code = self.generate_referral_code()
        while LoyaltyProgram.objects.filter(referral_code=referral_code).exists():
            referral_code = self.generate_referral_code()
        return referral_code

    def __str__(self):
        return f"{self.user} - {self.referral_code} - {self.balance}"


class LoyaltyTransaction(models.Model):
    """
    Модель транзакции в программе лояльности.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    points = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Баллы'),
    )
    description = models.CharField(max_length=255, verbose_name=_('Описание'), default='Automated transaction')
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата'))

    class Meta:
        verbose_name = _('Транзакция лояльности')
        verbose_name_plural = _('Транзакции лояльности')

    def __str__(self):
        return f"{self.user} - {self.points} - {self.date}"


# Импорт сигналов
from . import signals  # noqa F401