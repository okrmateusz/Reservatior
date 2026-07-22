from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("api/csrf", views.csrf_token, name="csrf"),
    path("api/register", views.register, name="register"),
    path("api/login", views.login_view, name="login"),
]
