import json

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST


def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})


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
    password_confirmation = str(data.get("passwordConfirmation", ""))

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": "Podaj poprawny adres e-mail."}, status=400)

    if password != password_confirmation:
        return JsonResponse({"error": "Hasła nie są takie same."}, status=400)

    user_model = get_user_model()
    user_candidate = user_model(username=email, email=email)

    try:
        validate_password(password, user=user_candidate)
    except ValidationError as error:
        return JsonResponse({"error": " ".join(error.messages)}, status=400)

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
