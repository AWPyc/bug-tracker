# 🐞 Bug Tracker API

RESTful API for managing software bug reports.
Supports creation, modification, deletion and tagging of bug entries.

---

## 🧰 Tech Stack

- **Python 3.12**
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM for database management
- **PostgreSQL** - relational database
- **Pytest** - testing framework
- **Ruff** - Python linter
- **Docker + Docker Compose** - containerized development & deployment
- **GitHub Actions** - CI for automated testing & linting

---

## 🔧 Features

- Full CRUD support for bug entries
- Tagging support (many-to-many relationship)
- Full support for REST methods: `GET`, `POST`, `PATCH`, `PUT`, `DELETE`
- Pydantic-powered validation for request payloads
- Automatic deduplication of tags
- Full unit & integration test coverage
- GitHub Actions for CI: automatic lint/test execution on each push or PR

---

## ️🗝️ Environment
`.env` is **not pushed** to version control.

Use `.env.example` to set up your own local version.

Secrets used in CI (GitHub Actions) are injected as environment variables.

---

## ▶️ Local launch (Docker)

1. Copy .env file:
    ```bash
    cp .env.example .env
   ```
   
2. Configure .env file with your DB credentials.

3. Build & run the app:
    ```bash
   docker compose up --build
   ```
   
4. App available at:
    ```
   http://localhost:8000
    ```
   
5. PGAdmin interface at:
    ```
   http://localhost:5050
    ```
   
## ✅ Testing

1. Run tests locally:
    ```bash
   pytest --maxfail=1 --disable-warnings
    ```
2. Run lint check:
    ```bash
   ruff check .
   ```
   
## 🔄 CI - GitHub Actions
Every push and pull request triggers:
- Lint check (Ruff)
- Test suite (Pytest)

Workflow config:
    ```
    bug_tracker/.github/workflows/ci.yml
    ```
