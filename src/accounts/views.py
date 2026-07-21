import json

from django.contrib.auth import authenticate, get_user_model, login
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


def index(request):
    return render(request, "accounts/index.html")


def request_data(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


@require_POST
def register(request):
    data = request_data(request)
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    user_model = get_user_model()

    try:
        user = user_model.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
    except (IntegrityError, ValueError):
        return JsonResponse({"error": "Nie udało się utworzyć konta."}, status=400)

    return JsonResponse(
        {"user": {"id": user.id, "email": user.email}},
        status=201,
    )


@require_POST
def login_view(request):
    data = request_data(request)
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    user = authenticate(request, username=email, password=password)

    if user is None:
        return JsonResponse(
            {"error": "Nieprawidłowy e-mail lub hasło."},
            status=401,
        )

    login(request, user)
    return JsonResponse({"user": {"id": user.id, "email": user.email}})
