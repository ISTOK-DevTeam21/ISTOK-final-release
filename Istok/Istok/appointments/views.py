from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import View
from .models import Appointment, Status
from users.models import User
from datetime import date, datetime, timedelta


@login_required
def calendar_view(request):
    """
    Представление для записи на встречу с сотрудником
    """
    start_day_for_booking = date.today() + timedelta(days=1)
    days = [start_day_for_booking + timedelta(days=i) for i in range(30)]
    format_days = [d.strftime('%Y-%m-%d') for d in days]
    work_time_list = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]
    specialists = User.objects.filter(groups__name__in=['Consultants', 'Designers', 'Measurers'])
    appointments = Appointment.objects.all()
    appointments_by_day = {}
    for day in format_days:
        appointments_by_day[day] = {
            hour: appointments.filter(date=day, time=hour).exists() for hour in work_time_list
        }
    query = request.GET.get('q')
    specialist_type = request.GET.get('type')
    if query:
        specialists = specialists.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(patronymic__icontains=query))
    if specialist_type:
        specialists = specialists.filter(groups__name__in=[specialist_type])

    if request.method == "POST":
        try:
            specialist_id = request.POST.get('specialist')
            appointment_date_str = request.POST.get('date')
            appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()
            appointment_time = request.POST.get('time')
            try:
                specialist = User.objects.get(id=specialist_id)
            except User.DoesNotExist:
                return redirect('book-appointment')
            if not Appointment.objects.filter(staff_user=specialist, date=appointment_date, time=appointment_time).exists():
                Appointment.objects.create(client_user=request.user, staff_user=specialist, status=Status.objects.get(status_name='not_commited'), date=appointment_date, time=appointment_time, is_booked=True)
        except ValueError:
            return redirect('book-appointment')
        return redirect('user_appointments')
    context = {
        'work_time_list': work_time_list,
        'specialists': specialists,
        'appointments_by_day':  appointments_by_day,
    }
    return render(request, 'main-page/calendar.html', context=context)


class UserAppointments(View):
    """
    Представление для вывода всех забронированных встреч пользователя
    """
    def get(self, request):
        appointments = Appointment.objects.filter(client_user=request.user.id).order_by('-created_at')
        context = {
            'appointments': appointments
        }
        return render(request, 'appointments/appointments_of_user.html', context=context)
