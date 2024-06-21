from django.urls import path
from .views import calendar_view
from .views import UserAppointments


urlpatterns = [
    path('calendar/', calendar_view, name='book-appointment'),
    path('your/appointments/', UserAppointments.as_view(), name='user_appointments')
]
