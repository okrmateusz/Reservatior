from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/register", views.register, name="register"),
    path("api/login", views.login_view, name="login"),
]
