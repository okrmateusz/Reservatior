# Reservatior

Monorepo systemu rezerwacji. Obecnie zaimplementowany jest backend Django z
rejestracją i logowaniem; pozostałe katalogi wyznaczają granice przyszłych
aplikacji bez dodawania ich implementacji.

## Struktura

```text
.
├── apps/
│   ├── web/
│   │   ├── business-panel/       # przyszły panel firmowy
│   │   └── booking-portal/       # przyszły portal rezerwacyjny
│   └── mobile/                   # przyszła aplikacja mobilna
├── backend/
│   ├── manage.py                 # polecenia administracyjne Django
│   ├── config/                   # ustawienia, routing oraz WSGI/ASGI
│   ├── apps/
│   │   ├── accounts/             # działająca rejestracja i logowanie
│   │   ├── organizations/        # przyszłe moduły domenowe
│   │   ├── employees/
│   │   ├── customers/
│   │   ├── services/
│   │   ├── schedules/
│   │   ├── bookings/
│   │   ├── notifications/
│   │   ├── payments/
│   │   └── subscriptions/
│   └── requirements/
│       ├── base.txt              # wspólne zależności Pythona
│       └── production.txt        # zależności produkcyjne
├── infrastructure/
│   ├── docker/Dockerfile         # obraz backendu
│   └── scripts/entrypoint.sh     # migracje przed startem aplikacji
├── docker-compose.yml            # lokalny backend i PostgreSQL
├── .env.example
└── README.md
```

Katalogi oznaczone jako przyszłe są celowo puste. Nie są jeszcze aplikacjami
Django i nie są dodane do `INSTALLED_APPS`.

## Uruchomienie przez Docker

```powershell
docker compose up --build
```

Aplikacja będzie dostępna pod `http://127.0.0.1:8000`. Migracje Django są
wykonywane automatycznie przez `infrastructure/scripts/entrypoint.sh`.

```powershell
docker compose down
```

## Uruchomienie bez Dockera

Zainstaluj zależności i skonfiguruj `.env` na podstawie `.env.example`:

```powershell
python -m pip install -r backend/requirements/base.txt
Set-Location backend
python manage.py migrate
python manage.py runserver
```

Testy i kontrola konfiguracji uruchamiane z katalogu `backend/`:

```powershell
python manage.py check
python manage.py test
```

## Render z Dockerem

Utwórz Docker Web Service i ustaw:

```text
Dockerfile Path: infrastructure/docker/Dockerfile
Health Check Path: /
```

Wymagane zmienne środowiskowe:

```text
DATABASE_URL=<Internal Database URL z Render PostgreSQL>
SESSION_SECRET=<wygenerowany sekret>
DJANGO_DEBUG=false
```

Kontener korzysta z `PORT` przekazanego automatycznie przez Render.
