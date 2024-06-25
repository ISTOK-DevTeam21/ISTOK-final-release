from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, View
from django.utils.translation import gettext_lazy as _

from accounts.forms import SignUpForm, PhoneNumberForm, PasswordForm

User = get_user_model()


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def login_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            phone_number_str = phone_number.as_e164
            request.session['phone_number'] = phone_number_str

            new_password = get_random_string(length=4, allowed_chars='0123456789')
            request.session['password'] = new_password
            print(f'{new_password}: ваш пароль для входа на сайт Istok.')

            return redirect('enter_password')  # Переходим ко второму шагу
        else:
            return render(request, 'registration/login.html', {'form': form})

    # Обработка GET запроса
    form = PhoneNumberForm()
    return render(request, 'registration/login.html', {'form': form})


def password_view(request):
    def generate_new_password():
        new_password = get_random_string(length=4, allowed_chars='0123456789')
        request.session['password'] = new_password
        request.session['attempt_count'] = 0  # Сбрасываем счетчик попыток
        print(f'{new_password} ваш пароль для входа на сайт Istok.')

    if 'phone_number' not in request.session:
        return redirect('login')  # Если нет номера телефона в сессии, переходим на первый шаг

    if request.session['password'] is None:
        generate_new_password()

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            phone_number_str = request.session['phone_number']

            # Проверяем, является ли введенный пароль сгенерированным паролем из сессии
            if password == request.session['password']:
                # Аутентификация пользователя
                user = User.objects.filter(phone_number=phone_number_str).first()
                if user is not None:
                    login(request, user)  # Логин пользователя
                    del request.session['phone_number']  # Удаляем phone_number из сессии после успешной авторизации
                    del request.session['password']  # Удаляем password из сессии после успешной авторизации
                    return redirect('main_page_index')
            else:
                error_message = _('Неверный пароль.')
                # Увеличиваем счетчик попыток
                request.session['attempt_count'] = request.session.get('attempt_count', 0) + 1

                # Если количество попыток достигло 10, генерируем новый пароль
                if request.session['attempt_count'] == 10:
                    generate_new_password()

                return render(request, 'registration/login_sms.html', {'form': form, 'error_message': error_message})

    else:
        form = PasswordForm()

    return render(request, 'registration/login_sms.html', {'form': form})
