# Reservatior

Monorepo systemu rezerwacji dla firm. Interfejs jest aplikacją Next.js, a
backend Django udostępnia API rejestracji i logowania.

## Struktura

```text
.
├── apps/
│   ├── web/
│   │   └── business-panel/       # Next.js App Router i proxy API
│   └── mobile/                   # przyszła aplikacja mobilna dla firm
├── backend/
│   ├── manage.py                 # polecenia administracyjne Django
│   ├── config/                   # ustawienia, routing oraz WSGI/ASGI
│   ├── apps/
│   │   ├── accounts/             # API rejestracji i logowania
│   │   ├── organizations/        # przyszłe moduły domenowe
│   │   ├── employees/
│   │   ├── customers/
│   │   ├── services/
│   │   ├── schedules/
│   │   ├── bookings/
│   │   ├── notifications/
│   │   ├── payments/
│   │   └── subscriptions/
│   ├── requirements/
│   │   ├── base.txt              # wspólne zależności Pythona
│   │   ├── development.txt       # pytest i narzędzia lokalne
│   │   └── production.txt        # zależności produkcyjne
│   └── tests/                    # wszystkie testy backendu według zachowania
├── infrastructure/
│   ├── docker/Dockerfile         # obraz backendu Django
│   ├── docker/web.Dockerfile     # obraz frontendu Next.js
│   └── scripts/entrypoint.sh     # migracje przed startem aplikacji
├── docker-compose.yml            # lokalny web, backend i PostgreSQL
├── .env.example
└── README.md
```

Katalogi oznaczone jako przyszłe są celowo puste. Nie są jeszcze aplikacjami
Django i nie są dodane do `INSTALLED_APPS`.

## Uruchomienie przez Docker

```powershell
docker compose up --build
```

Panel będzie dostępny pod `http://127.0.0.1:3000`, a API Django pod
`http://127.0.0.1:8000`. Migracje Django są wykonywane automatycznie przez
`infrastructure/scripts/entrypoint.sh`.

```powershell
docker compose down
```

## Uruchomienie bez Dockera

Skonfiguruj główny `.env` na podstawie `.env.example`, a następnie uruchom
backend:

```powershell
python -m pip install -r backend/requirements/development.txt
Set-Location backend
python manage.py migrate
python manage.py runserver
```

W drugim terminalu uruchom frontend:

```powershell
Set-Location apps/web/business-panel
Copy-Item .env.example .env.local
npm install
npm run dev
```

Testy i kontrola konfiguracji uruchamiane z katalogu `backend/`:

```powershell
python manage.py check
python manage.py test
```

Testy można również uruchamiać przez pytest z katalogu głównego, w tym przez
panel Testing w Visual Studio Code:

```powershell
python -m pytest
python -m pytest backend/tests/test_registration.py
```

Kontrola frontendu:

```powershell
npm run lint
npm run build
```

## Render z Dockerem

Utwórz osobny Docker Web Service dla backendu:

```text
Dockerfile Path: infrastructure/docker/Dockerfile
Health Check Path: /
```

Wymagane zmienne środowiskowe:

```text
DATABASE_URL=<Internal Database URL z Render PostgreSQL>
SESSION_SECRET=<wygenerowany sekret>
DJANGO_DEBUG=false
FRONTEND_URL=https://<adres-frontendu>.onrender.com
```

Utwórz drugi Docker Web Service dla frontendu:

```text
Dockerfile Path: infrastructure/docker/web.Dockerfile
Health Check Path: /
BACKEND_URL=https://<adres-backendu>.onrender.com
```

Oba kontenery korzystają z `PORT` przekazanego automatycznie przez Render.
