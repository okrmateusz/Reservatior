# Reservatior

Prosta aplikacja Django udostępniająca rejestrację i logowanie użytkowników.

## Struktura

```text
.
├── src/                        # cały kod wykonywalny aplikacji
│   ├── manage.py               # polecenia administracyjne Django
│   ├── reservatior/            # konfiguracja całego projektu
│   │   ├── settings.py         # ustawienia środowiska, bazy i middleware
│   │   ├── urls.py             # główny routing
│   │   ├── asgi.py             # punkt wejścia ASGI
│   │   └── wsgi.py             # punkt wejścia WSGI/Gunicorn
│   └── accounts/               # funkcjonalność kont użytkowników
│       ├── migrations/         # przyszłe migracje modeli tej aplikacji
│       ├── templates/accounts/ # szablony należące do accounts
│       ├── apps.py             # konfiguracja aplikacji Django
│       ├── urls.py             # routing rejestracji i logowania
│       └── views.py            # widoki i endpointy JSON
├── tests/                      # testy odzwierciedlające moduły z src/
│   └── test_accounts.py        # testy rejestracji i logowania
├── requirements.txt            # zależności Pythona
└── .env.example                # przykładowa konfiguracja lokalna
```

`reservatior` konfiguruje projekt, natomiast `accounts` zawiera konkretną
funkcjonalność. Nowe funkcje domenowe powinny trafiać do osobnych aplikacji
Django obok `accounts` w katalogu `src/`.

## Uruchomienie lokalne

Skopiuj `.env.example` do `.env`, a następnie wykonaj:

```powershell
python src/manage.py migrate
python src/manage.py runserver
```

Testy i kontrola konfiguracji:

```powershell
python src/manage.py check
python src/manage.py test
```

## Render

```text
Build Command: pip install -r requirements.txt && python src/manage.py migrate
Start Command: python -m gunicorn --chdir src reservatior.wsgi:application
```
