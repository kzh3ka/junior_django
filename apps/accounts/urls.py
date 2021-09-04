from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import LoginView, logout


urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", logout),
]
