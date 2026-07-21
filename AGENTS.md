# Repository Guidelines

## Project Structure & Module Organization

This repository is currently an empty scaffold. Keep the root focused on project-wide configuration and documentation. As implementation is added, use a predictable layout:

- `src/` for application code, grouped by feature or domain.
- `tests/` for automated tests that mirror the structure under `src/`.
- `assets/` for static files such as images, fixtures, and templates.
- `docs/` for architecture notes and longer operational guidance.

Avoid placing generated output or dependencies in version control. Add tool-specific directories such as `dist/`, `coverage/`, and dependency caches to `.gitignore`.

## Build, Test, and Development Commands

No build system or package manifest has been committed yet. When selecting the toolchain, expose a small, consistent command set and document it in `README.md`. Prefer commands with clear responsibilities, for example:

- `python src/manage.py runserver` starts the local development server.
- `python src/manage.py migrate` applies database migrations.
- `python src/manage.py test` runs the complete automated test suite.
- `python src/manage.py check` checks the Django configuration.

Do not commit code that depends on undocumented one-off setup steps.

## Coding Style & Naming Conventions

Use the formatter and linter standard to the chosen language, and commit their configuration at the repository root. Default to spaces, UTF-8, LF line endings, and a final newline. Use descriptive names: `PascalCase` for types and components, `camelCase` for functions and variables, and `kebab-case` for general file names unless the framework dictates otherwise. Keep modules focused and avoid hidden side effects.

## Testing Guidelines

Add tests with every behavior change and bug fix. Name tests after the unit or scenario they verify (for example, `reservation-service.test.ts`). Cover success paths, validation failures, and boundary cases. Tests must be deterministic and must not depend on shared external services; use fixtures or mocks where appropriate.

## Commit & Pull Request Guidelines

There is no Git history from which to infer an established convention. Use concise, imperative commit subjects, optionally following Conventional Commits, such as `feat: add reservation validation` or `fix: reject overlapping bookings`. Keep each commit focused.

Pull requests should explain the problem and solution, list verification performed, and link relevant issues. Include screenshots for visual changes and call out configuration changes, migrations, or follow-up work. Request review only after local checks pass.

## Security & Configuration

Never commit secrets or local environment files. Provide sanitized examples such as `.env.example`, validate configuration at startup, and document every required variable.

# Repository Guidelines

## Project Structure & Module Organization

Application code lives in `app/`. `app/main.py` defines FastAPI routes, while `mail.py`, `calendar.py`, and `config.py` isolate integrations and settings. Server-rendered Jinja templates are under `app/templates/`. Tests live in `tests/` and generally mirror application areas, for example `tests/test_mail.py`. Database documentation and the baseline PostgreSQL schema are in `DATABASE.md` and `db/init.sql`. Operational utilities belong in `scripts/`; runtime data and logs belong in `data/` and `logs/` and should not be committed.

## Build, Test, and Development Commands

Use Docker Compose for all development tasks; a host Python environment is not required.

- `docker compose up --build` builds and runs the app and PostgreSQL at `http://127.0.0.1:8010`.
- `docker compose up --build -d` starts the stack in the background.
- `docker compose logs -f mail-client` follows application logs.
- `docker compose run --rm mail-client python -m pytest` runs the complete test suite in a container.
- `docker compose run --rm mail-client python scripts/smtp_check.py [recipient@example.com]` checks SMTP and optionally sends a test message.
- `docker compose down` stops the stack without deleting PostgreSQL data.

## Coding Style & Naming Conventions

Use Python 3 conventions: four-space indentation, type hints for service boundaries and data objects, `snake_case` for functions and modules, and `PascalCase` for classes. Keep route handlers thin and move mail, calendar, configuration, or database logic into focused modules. Follow the existing import grouping (standard library, third-party, local) and keep templates named after their route purpose. No formatter or linter is currently configured; write PEP 8-compatible code and avoid unrelated formatting changes.

## Testing Guidelines

Tests use pytest and FastAPI's `TestClient`. Name files `test_<area>.py` and tests `test_<behavior>()`. Mock external IMAP, SMTP, Google, and database interactions; tests must not depend on real credentials or network access. Add regression tests with every behavior change. Run `docker compose run --rm mail-client python -m pytest` before submitting work.

## Database Schema Changes

Do not create incremental migrations. Keep the complete PostgreSQL schema in `db/init.sql`. After every schema change, reset the local database with `docker compose down -v`, then rebuild it with `docker compose up --build`. The reset permanently removes local database contents, so confirm that no development data must be preserved before running it.

## Commit & Pull Request Guidelines

Use Conventional Commits with lowercase types and imperative, concise descriptions: `feat: add calendar event filtering`, `fix: handle SMTP timeout`, `test: cover invalid OAuth callback`, or `docs: update Docker setup`. Common types are `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, and `build`; add a scope when useful, for example `fix(mail): preserve message encoding`. Mark incompatible changes with `!` and explain them in the commit body. Keep each commit focused. Pull requests should explain the user-visible change, list configuration or schema impacts, and include test results. Link relevant issues and attach screenshots for template or UI changes. Call out all edits to `db/init.sql`.

## Security & Configuration

Copy `.env.example` to `.env`; never commit `.env`, OAuth tokens, client secrets, mail credentials, or generated logs. Use strong PostgreSQL passwords outside local development and retain Google Calendar's read-only scope unless a change is explicitly reviewed.


## Working philosophy

Work in small, controlled, incremental steps.

The goal is not to complete an entire feature unless the task explicitly requests a complete feature.

Prefer the smallest coherent change that produces the explicitly requested result while preserving the correctness of the existing system.

Analyze as much context as necessary, but modify as little as necessary.

## Scope rules

Treat the user's request as the complete scope of the current task.

Anything not explicitly requested is out of scope, even when it:

* seems useful,
* is a common best practice,
* would make the feature more complete,
* would improve production readiness,
* may be needed in a future step,
* is easy to add while editing nearby code.

Do not interpret omitted requirements as implicit requirements.

Treat intentional incompleteness as valid.

Do not complete the surrounding feature unless explicitly asked.

## Before making changes

Before editing code, determine:

1. The single observable result requested by the user.
2. The smallest coherent implementation that can produce that result.
3. Which files must be changed.
4. Which files may need to be inspected but do not need to be changed.
5. Which possible improvements are optional and therefore out of scope.

Internally classify possible changes into:

### Necessary

A change is necessary only when omitting it would:

* prevent the requested behavior from working,
* cause the code not to compile or run,
* break an existing contract,
* violate an existing invariant,
* leave persistent data in an inconsistent state,
* introduce a direct regression in an existing supported path.

### Optional

A change is optional when it:

* improves completeness,
* handles additional cases not mentioned in the task,
* prepares code for future requirements,
* introduces a new abstraction,
* improves architecture without being required,
* adds convenience behavior,
* improves styling beyond the requested result,
* adds production-readiness features,
* addresses unrelated technical debt.

Do not implement optional changes.

### Unrelated

A change is unrelated when it addresses a problem discovered while working but does not directly affect the requested result.

Do not implement unrelated changes.

## Minimal coherent change

Do not optimize for the smallest number of changed lines.

Optimize for the smallest coherent change.

A change may involve multiple files when this is strictly required by an existing contract, data model, invariant, or build process.

A larger scope is justified only when a local change would:

* break compilation,
* break an existing interface,
* break an existing caller,
* make data inconsistent,
* violate an established domain rule,
* create an immediate runtime failure,
* leave the requested behavior unusable.

The following are not sufficient reasons to expand the scope:

* future usefulness,
* elegance,
* consistency with an ideal architecture,
* anticipated requirements,
* general best practices,
* convenience,
* production completeness,
* personal preference.

For every modified file, there must be a direct and specific reason why the requested result requires that modification.

If that reason cannot be stated clearly, do not modify the file.

## Implementation rules

Implement only the explicitly requested behavior.

Do not:

* anticipate future requirements,
* add code for later use,
* create unused components,
* create unused functions,
* create unused data structures,
* add extension points,
* add generic abstractions,
* add configuration options that were not requested,
* add dependencies unless strictly required,
* refactor adjacent code without necessity,
* rename unrelated symbols,
* reorganize files,
* change formatting outside the modified area,
* improve unrelated error handling,
* improve unrelated security,
* add analytics,
* add telemetry,
* add caching,
* add persistence,
* add database integration,
* add API integration,
* add authentication,
* add authorization,
* add validation,
* add loading states,
* add error states,
* add retry logic,
* add accessibility enhancements,
* add responsive behavior,
* add tests,
* update documentation,

unless the task explicitly requests them or they are strictly necessary for the requested change to work without breaking the existing system.

When the task asks for a UI element, create only that UI element and only the behavior explicitly described.

For example, if the task asks for:

* an input, do not automatically add validation;
* a button, do not automatically add click behavior;
* a form, do not automatically connect it to an API;
* a login screen, do not automatically implement authentication;
* a data field, do not automatically add persistence;
* an endpoint, do not automatically build a frontend for it.

## Interpretation rules

When multiple valid interpretations exist, choose the interpretation that:

1. adds the least new behavior,
2. changes the fewest existing assumptions,
3. introduces the least new code,
4. affects the smallest number of components,
5. is easiest to extend in a later explicit step.

Do not choose the most complete interpretation.

Do not infer product requirements from conventions.

Do not infer hidden requirements from the name of a feature.

For example, the phrase “login form” does not automatically include:

* database access,
* session management,
* password reset,
* remember-me functionality,
* validation,
* rate limiting,
* OAuth,
* token handling,
* redirects,
* error messages.

These elements are separate tasks unless explicitly requested.

## Existing architecture

Follow existing project conventions when doing so does not materially expand the change.

Reuse an existing abstraction when it already fits the requested behavior.

Do not create a new abstraction merely because similar code may appear later.

A small amount of duplication is preferable to a premature abstraction when the future requirement is not yet known.

Do not redesign existing architecture as part of a feature task.

If the current architecture makes the requested change difficult, make the smallest compatible change. Report the architectural limitation instead of redesigning the system.

## Context inspection

You may inspect any files needed to understand the task.

Reading a file does not imply permission to modify it.

Use broader context to identify contracts, callers, invariants, and side effects.

Do not turn broad analysis into broad implementation.

## Tests and verification

Run relevant existing checks when practical.

Do not automatically add new tests unless:

* the user explicitly requests tests,
* the repository rules explicitly require them,
* the requested behavior cannot be safely changed without updating an existing test,
* an existing test must change because the requested behavior intentionally changes its contract.

Do not expand the production implementation merely to satisfy unrelated failing tests.

Report unrelated failures separately.

## When the requested change requires broader work

If the task cannot be implemented as a small coherent change, do not silently expand it into a complete feature.

Instead:

1. identify the exact dependency, contract, or invariant causing the expansion;
2. distinguish necessary changes from optional changes;
3. implement only the necessary changes;
4. report why each additional modification was required.

Do not use “best practice” as the sole justification for expanding scope.

## Stop condition

Stop immediately when the explicitly requested observable result works and the existing system remains coherent.

Do not continue with:

* cleanup,
* polish,
* additional cases,
* future-proofing,
* optional safeguards,
* adjacent improvements,
* convenience features.

A deliberately incomplete feature is acceptable when the current task requests only one incremental step.

## Final report

After completing the task, report:

1. what was changed;
2. which observable result was implemented;
3. which files were modified;
4. why each modified file was necessary;
5. what was intentionally not implemented;
6. what checks were run;
7. any assumptions or limitations.

Do not present optional work as completed work.

Do not suggest that an incomplete feature is complete.

Clearly distinguish the current increment from possible future steps.
