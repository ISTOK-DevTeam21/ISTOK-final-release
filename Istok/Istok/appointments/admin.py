from django.contrib import admin
from .models import Status, Appointment


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_status_name_display')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff_user', 'client_user', 'status', 'created_at')


admin.site.register(Status, StatusAdmin)
admin.site.register(Appointment, AppointmentAdmin)
