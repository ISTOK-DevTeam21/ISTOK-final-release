from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import LoyaltyProgram, LoyaltyTransaction, User, Room


class RoomInline(admin.TabularInline):
    model = User.repair_rooms.through
    extra = 1


class UserAdmin(BaseUserAdmin):
    """
    Админ-панель для управления пользователями.
    """
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Персональная информация'), {'fields': ('first_name', 'last_name', 'patronymic', 'email', 'birth_date')}),
        (_('Дополнительная информация'), {'fields': (
            'has_children', 'repair_planned', 'repair_date', 'repair_rooms', 'subscribe_newsletter',
            'consent_personal_data',
        )}),
        (_('Права доступа'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('phone_number', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    ordering = ('last_name', 'first_name', 'phone_number')


class LoyaltyProgramAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления программами лояльности.
    """
    list_display = ('user', 'balance', 'referral_code')

    fieldsets = (
        (None, {'fields': ('user', 'balance')}),
    )
    search_fields = ('user__phone_number', 'user__email', 'user__first_name', 'user__last_name')
    ordering = ('user__last_name', 'user__first_name', 'user__phone_number')


class LoyaltyTransactionAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления транзакциями лояльности.
    """
    list_display = ('user', 'points', 'description', 'date')
    search_fields = ('user__phone_number', 'description', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('date', 'points')
    ordering = ('date', 'user__last_name', 'user__first_name', 'user__phone_number')


admin.site.register(User, UserAdmin)
admin.site.register(LoyaltyProgram, LoyaltyProgramAdmin)
admin.site.register(LoyaltyTransaction, LoyaltyTransactionAdmin)
admin.site.register(Room)
