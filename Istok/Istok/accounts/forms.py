from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import RegionalPhoneNumberWidget

User = get_user_model()


class PhoneNumberForm(forms.Form):
    phone_number = PhoneNumberField(
        label='',
        required=True,
        widget=RegionalPhoneNumberWidget(attrs={
            'class': 'login__input',
            'placeholder': '+7 (999) 999-99-99'
        })
    )


class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_('Пароль'),
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'login__input',
            'placeholder': 'Введите пароль'
        })
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) != 4 or not password.isdigit():
            raise forms.ValidationError('Пароль должен состоять из 4 цифр.')
        return password


class SignUpForm(UserCreationForm):
    phone_number = PhoneNumberField(label=_('Номер телефона'), required=True)

    class Meta:
        model = User
        fields = ('phone_number', 'password1', 'password2')
