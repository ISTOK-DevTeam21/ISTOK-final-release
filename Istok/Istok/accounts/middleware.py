# accounts/middleware.py

from django.shortcuts import redirect
from django.urls import reverse


class EnsureFirstNameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.first_name:
            if request.path != reverse('account_firstname_update') and not request.path.startswith('/admin/'):
                return redirect('account_firstname_update')

        response = self.get_response(request)
        return response
