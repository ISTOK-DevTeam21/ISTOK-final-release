from django.urls import path, include

from accounts.views import SignUp, login_view, password_view, UpdateFirstNameView, logout_view

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('enter_password/', password_view, name='enter_password'),
    path('', include('django.contrib.auth.urls')),
    path('update-first-name/', UpdateFirstNameView.as_view(), name='account_firstname_update'),
    path('logout/', logout_view, name='logout'),
]