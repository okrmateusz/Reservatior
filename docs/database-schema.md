# Obecny schemat bazy danych

Diagram przedstawia aktualny schemat PostgreSQL tworzony przez wbudowane
migracje Django. Projekt nie zawiera jeszcze własnych tabel domenowych.

```mermaid
erDiagram
    auth_user {
        integer id PK
        varchar_128 password
        timestamptz last_login "NULL"
        boolean is_superuser
        varchar_150 username UK
        varchar_150 first_name
        varchar_150 last_name
        varchar_254 email
        boolean is_staff
        boolean is_active
        timestamptz date_joined
    }

    auth_group {
        integer id PK
        varchar_150 name UK
    }

    django_content_type {
        integer id PK
        varchar_100 app_label "UK: app_label + model"
        varchar_100 model "UK: app_label + model"
    }

    auth_permission {
        integer id PK
        varchar_255 name
        integer content_type_id FK "UK: content_type_id + codename"
        varchar_100 codename "UK: content_type_id + codename"
    }

    auth_user_groups {
        bigint id PK
        integer user_id FK "UK: user_id + group_id"
        integer group_id FK "UK: user_id + group_id"
    }

    auth_user_user_permissions {
        bigint id PK
        integer user_id FK "UK: user_id + permission_id"
        integer permission_id FK "UK: user_id + permission_id"
    }

    auth_group_permissions {
        bigint id PK
        integer group_id FK "UK: group_id + permission_id"
        integer permission_id FK "UK: group_id + permission_id"
    }

    django_session {
        varchar_40 session_key PK
        text session_data
        timestamptz expire_date
    }

    django_migrations {
        bigint id PK
        varchar_255 app
        varchar_255 name
        timestamptz applied
    }

    django_content_type ||--o{ auth_permission : "content_type_id"
    auth_user ||--o{ auth_user_groups : "user_id"
    auth_group ||--o{ auth_user_groups : "group_id"
    auth_user ||--o{ auth_user_user_permissions : "user_id"
    auth_permission ||--o{ auth_user_user_permissions : "permission_id"
    auth_group ||--o{ auth_group_permissions : "group_id"
    auth_permission ||--o{ auth_group_permissions : "permission_id"
```

`django_session` nie ma klucza obcego do `auth_user`: dane użytkownika są
przechowywane wewnątrz zakodowanego pola `session_data`. `django_migrations`
jest technicznym rejestrem wykonanych migracji i również nie ma relacji z
pozostałymi tabelami.
