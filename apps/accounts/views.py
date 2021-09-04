from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import (
    authenticate as _authenticate,
    login as _login,
    logout as _logout,
)
from django.views import View

from .forms import LoginForm


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors)

        cleaned_data = form.cleaned_data
        user = _authenticate(
            username=cleaned_data["username"],
            password=cleaned_data["password"],
        )
        if user is None or not user.is_active:
            return HttpResponseBadRequest("User not found")

        _login(request, user)
        return HttpResponse("Authenticated successfully")


def logout(request):
    _logout(request)
