# 🎟️ Event Ticket Booking System

> 🚧 **Work in progress.** This project is still being built. Some features are only partly done, the API may change, and parts of this README are unfinished. See the [Roadmap](#-roadmap) for what's still to come.

A REST API backend for booking event tickets, built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. Users can sign up, browse venues and their events, look at seats, and book a seat for an event.

---

## 📑 Table of Contents

- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Data Model](#-data-model)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [Roadmap](#-roadmap)
- [Known Limitations](#-known-limitations)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🛠 Tech Stack

| Layer            | Technology                                   |
| ---------------- | -------------------------------------------- |
| Language         | Python 3.13                                  |
| Web framework    | FastAPI                                      |
| Database         | PostgreSQL 17                                |
| ORM / migrations | SQLAlchemy 2.x, Alembic                      |
| Validation       | Pydantic v2, pydantic-settings               |
| Auth             | OAuth2 password flow + JWT (`python-jose`)   |
| Password hashing | `pwdlib` (Argon2)                            |
| Cache / locking  | Redis *(set up, not wired in yet)*           |
| Packaging        | `uv` (`pyproject.toml`, `uv.lock`)           |
| Containers       | Docker, Docker Compose                       |

---

## ✨ Features

### ✅ Done

- **Users:** register, log in with a JWT, view, update, and delete your own profile
- **Venues:** create a venue, list all venues, get one venue
- **Events:** create, list (by venue), get, update, and delete events
- **Seats:** list the seats at a venue
- **Bookings:** book a seat for an event, list your bookings, get one, cancel one
- Row-level lock (`SELECT ... FOR UPDATE`) on the seat while a booking is made
- Layered design: routes → services → repositories → models
- Alembic migrations
- Docker and Docker Compose setup with Postgres

### 🔨 In progress / planned

- Temporary seat holds using Redis (`hold_expires_at` exists on bookings but isn't used yet)
- Booking status flow (`pending` → `confirmed` / `cancelled` / `expired`)
- Endpoints for creating and managing seats
- Role-based access (admin-only venue and event management)
- *More coming soon…*

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI app and router registration
│   ├── api/
│   │   ├── deps.py          # Shared dependencies (current user)
│   │   └── routes/          # user, venue, event, seat, booking routers
│   ├── core/
│   │   ├── config.py        # Settings loaded from .env
│   │   ├── security.py      # Password hashing, JWT create/verify
│   │   └── exceptions.py    # (placeholder)
│   ├── db/
│   │   ├── database.py      # Engine and declarative Base
│   │   └── session.py       # SessionLocal and get_db dependency
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic
│   ├── repositories/        # Database access
│   └── redis/               # Redis client (WIP)
├── alembic/                 # Migration environment and versions
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

---

## 🗄 Data Model

```
Venue 1 ──── * Seat
  │              │
  1              1
  │              │
  *              *
Event 1 ──── * Booking * ──── 1 User
```

| Table      | Key columns                                                                          |
| ---------- | ------------------------------------------------------------------------------------ |
| `users`    | `id`, `name` (unique), `email` (unique, optional), password hash, `created_at`       |
| `venues`   | `id`, `name`, `location` — unique on (`name`, `location`)                            |
| `seats`    | `id`, `venue_id`, `row`, `seat_number` — unique on (`venue_id`, `row`, `seat_number`) |
| `events`   | `id`, `venue_id`, `name`, `description`, `event_date`, `start_time`, `end_time`, `ticket_price` |
| `bookings` | `id`, `user_id`, `event_id`, `seat_id`, `status`, `hold_expires_at`, `created_at`    |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (or `pip`)
- PostgreSQL 17 (or Docker)
- Redis *(not needed yet, but `REDIS_URL` must be set)*

### Option 1: Run locally

1. **Clone the repo**

   ```bash
   git clone <repo-url>
   cd "Event Ticket Booking System"
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables.** Copy `.env.example` to `.env` and fill it in (see [Environment Variables](#-environment-variables)).

4. **Run the migrations**

   ```bash
   uv run alembic upgrade head
   ```

5. **Start the server**

   ```bash
   uv run fastapi dev app/main.py
   ```

   The API runs at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

### Option 2: Run with Docker Compose

1. Create a `.env.docker` file containing the app variables plus the Postgres variables (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`). Use `db` as the database host in `DATABASE_URL`.
2. Build and start the containers:

   ```bash
   docker compose up --build
   ```

   The container runs `alembic upgrade head` on startup, then serves the API on port `8000`.

> ⚠️ The Compose file doesn't include a Redis service yet. See [Known Limitations](#-known-limitations).

---

## 🔐 Environment Variables

| Variable                      | Description                         | Example                                                    |
| ----------------------------- | ----------------------------------- | ---------------------------------------------------------- |
| `DATABASE_URL`                | SQLAlchemy database URL             | `postgresql+psycopg://user:pass@localhost:5432/ticketing`  |
| `SECRET_KEY`                  | Key used to sign JWTs               | `change-me`                                                |
| `ALGORITHM`                   | JWT signing algorithm               | `HS256`                                                    |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | How long an access token lasts      | `30`                                                       |
| `REDIS_URL`                   | Redis connection URL                | `redis://localhost:6379/0`                                 |

---

## 📡 API Endpoints

🔒 means the endpoint needs a `Bearer` token from `/user/login`.

### User

| Method | Endpoint         | Description                     | Auth |
| ------ | ---------------- | ------------------------------- | ---- |
| POST   | `/user/register` | Register a new user             |      |
| POST   | `/user/login`    | Log in (form data), get a JWT   |      |
| GET    | `/user/me`       | Get your profile                | 🔒   |
| PUT    | `/user/update`   | Update your profile             | 🔒   |
| DELETE | `/user/delete`   | Delete your account             | 🔒   |

### Venues

| Method | Endpoint            | Description        | Auth |
| ------ | ------------------- | ------------------ | ---- |
| POST   | `/venues/create`    | Create a venue     |      |
| GET    | `/venues/get`       | List all venues    |      |
| GET    | `/venues/get/{id}`  | Get a venue by ID  |      |

### Events

| Method | Endpoint                               | Description               | Auth |
| ------ | -------------------------------------- | ------------------------- | ---- |
| POST   | `/venues/{venue_id}/events`            | Create an event at a venue |      |
| GET    | `/venues/{venue_id}/events`            | List a venue's events     |      |
| GET    | `/venues/events/{event_id}`            | Get an event              |      |
| PUT    | `/venues/{venue_id}/events/{event_id}` | Update an event           |      |
| DELETE | `/venues/events/{event_id}`            | Delete an event           |      |

### Seats

| Method | Endpoint           | Description                | Auth |
| ------ | ------------------ | -------------------------- | ---- |
| GET    | `/venue/{id}/seat` | List the seats at a venue  |      |

### Bookings

| Method | Endpoint                 | Description            | Auth |
| ------ | ------------------------ | ---------------------- | ---- |
| POST   | `/bookings/post`         | Book a seat for an event | 🔒   |
| GET    | `/bookings/`             | List your bookings     | 🔒   |
| GET    | `/bookings/{booking_id}` | Get one of your bookings | 🔒   |
| DELETE | `/bookings/{booking_id}` | Cancel a booking       | 🔒   |

> 📝 Route names are not final and may be cleaned up into a consistent REST style (for example `POST /bookings` instead of `/bookings/post`).

<!-- TODO: add example requests and responses -->

---

## 🗺 Roadmap

- [x] User auth with JWT
- [x] Venue CRUD (create and read)
- [x] Event CRUD
- [x] Seat listing
- [x] Basic booking flow
- [x] Dockerize the application
- [ ] Redis-backed seat holds with expiry
- [ ] Booking confirmation and status lifecycle
- [ ] Seat management endpoints
- [ ] Admin roles and permissions
- [ ] Consistent route naming and versioning (`/api/v1`)
- [ ] Centralized exception handling
- [ ] Input validation (prices, event times)
- [ ] Unit and integration tests
- [ ] Payment integration
- [ ] CI/CD pipeline
- [ ] *To be decided…*

---

## ⚠️ Known Limitations

This is an unfinished project, so expect rough edges:

- Redis is configured but not used yet, and Docker Compose has no Redis service.
- There's no API for creating seats yet, so seats have to be added straight to the database.
- Venue and event endpoints have no authentication.
- There are no tests yet.

---
