from django.urls import path
from .views import calendar_view, available_time_slots, specialists_by_type


# URLs for appointments/
urlpatterns = [
    path('appointments/calendar/', calendar_view, name='calendar-view'),
    path('api/available-time-slots/', available_time_slots, name='available-time-slots'),
    path('api/specialists/', specialists_by_type, name='specialists-by-type'),

    path('calendar/', calendar_view, name='book-appointment'),
]
