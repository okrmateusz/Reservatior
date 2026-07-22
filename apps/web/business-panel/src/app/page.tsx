"use client";

import { FormEvent, useState } from "react";


type FormState = {
  message: string;
  pending: boolean;
};


const initialState: FormState = { message: "", pending: false };


async function getCsrfToken(): Promise<string> {
  const response = await fetch("/api/csrf", { credentials: "same-origin" });

  if (!response.ok) {
    throw new Error("Nie udało się pobrać tokenu CSRF.");
  }

  const data = await response.json();
  return data.csrfToken;
}


async function submitCredentials(endpoint: string, form: HTMLFormElement) {
  const data = new FormData(form);
  const csrfToken = await getCsrfToken();
  const firstName = data.get("firstName");
  const lastName = data.get("lastName");
  const passwordConfirmation = data.get("passwordConfirmation");

  return fetch(endpoint, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      ...(firstName !== null && { firstName }),
      ...(lastName !== null && { lastName }),
      email: data.get("email"),
      password: data.get("password"),
      ...(passwordConfirmation !== null && { passwordConfirmation }),
    }),
  });
}


async function getErrorMessage(response: Response, fallback: string) {
  const data: unknown = await response.json().catch(() => null);

  if (
    typeof data === "object" &&
    data !== null &&
    "error" in data &&
    typeof data.error === "string"
  ) {
    return data.error;
  }

  return fallback;
}


export default function Home() {
  const [registration, setRegistration] = useState(initialState);
  const [authentication, setAuthentication] = useState(initialState);

  async function register(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setRegistration({ message: "", pending: true });

    try {
      const response = await submitCredentials("/api/register", event.currentTarget);
      const message = response.ok
        ? "Konto zostało utworzone."
        : await getErrorMessage(response, "Nie udało się utworzyć konta.");

      setRegistration({
        message,
        pending: false,
      });
    } catch {
      setRegistration({ message: "Nie udało się połączyć z serwerem.", pending: false });
    }
  }

  async function authenticate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setAuthentication({ message: "", pending: true });

    try {
      const response = await submitCredentials("/api/login", event.currentTarget);
      setAuthentication({
        message: response.ok ? "Zalogowano." : "Nieprawidłowy e-mail lub hasło.",
        pending: false,
      });
    } catch {
      setAuthentication({ message: "Nie udało się połączyć z serwerem.", pending: false });
    }
  }

  return (
    <main className="page-shell">
      <section className="auth-card">
        <h1>Reservatior</h1>
        <p className="intro">Panel rezerwacji dla firm</p>

        <div className="forms">
          <form onSubmit={register}>
            <h2>Rejestracja</h2>

            <label htmlFor="registration-first-name">Imię</label>
            <input
              id="registration-first-name"
              maxLength={150}
              name="firstName"
              required
              type="text"
            />

            <label htmlFor="registration-last-name">Nazwisko</label>
            <input
              id="registration-last-name"
              maxLength={150}
              name="lastName"
              required
              type="text"
            />

            <label htmlFor="registration-email">E-mail</label>
            <input id="registration-email" name="email" type="email" />

            <label htmlFor="registration-password">Hasło</label>
            <input id="registration-password" name="password" type="password" />

            <label htmlFor="registration-password-confirmation">Powtórz hasło</label>
            <input
              id="registration-password-confirmation"
              name="passwordConfirmation"
              type="password"
            />

            <button disabled={registration.pending} type="submit">
              {registration.pending ? "Tworzenie…" : "Utwórz konto"}
            </button>
            <p aria-live="polite">{registration.message}</p>
          </form>

          <form onSubmit={authenticate}>
            <h2>Logowanie</h2>

            <label htmlFor="login-email">E-mail</label>
            <input id="login-email" name="email" type="email" />

            <label htmlFor="login-password">Hasło</label>
            <input id="login-password" name="password" type="password" />

            <button disabled={authentication.pending} type="submit">
              {authentication.pending ? "Logowanie…" : "Zaloguj się"}
            </button>
            <p aria-live="polite">{authentication.message}</p>
          </form>
        </div>
      </section>
    </main>
  );
}
