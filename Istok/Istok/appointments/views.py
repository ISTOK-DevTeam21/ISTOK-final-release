from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from users.models import User


@login_required
def calendar_view(request):
    context = {}
    return render(request, 'main-page/calendar.html', context=context)

def available_time_slots(request):
    date = request.GET.get('date')
    # Логика для получения свободных временных слотов на определенную дату
    time_slots = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00']
    return JsonResponse({'time_slots': time_slots})

def specialists_by_type(request):
    specialist_type = request.GET.get('type')
    # Логика для получения списка специалистов по типу
    specialists = User.objects.filter(groups__name=specialist_type)
    specialists_data = [{'id': specialist.id, 'name': specialist.get_full_name()} for specialist in specialists]
    return JsonResponse({'specialists': specialists_data})
