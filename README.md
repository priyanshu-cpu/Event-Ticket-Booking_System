# Event Ticket Booking System

An asynchronous REST API for managing venues, events, seats, and ticket bookings. Built with FastAPI, PostgreSQL, and Redis.

The application supports user registration, JWT authentication, temporary seat holds, and booking confirmation through a layered backend architecture.

> **Project status:** In development. Payment processing is simulated, and database initialization and booking reliability require further work before production use.

## Features

- User registration with Argon2 password hashing.
- JWT bearer authentication.
- Public venue, event, and seat listings.
- Administrator-restricted venue and event management.
- Booking creation with seat-to-venue validation.
- PostgreSQL seat row locking during booking creation.
- Redis-backed temporary seat holds.
- Booking history scoped to the authenticated user.
- Booking confirmation and expiry handling.
- Interactive API documentation.

## Technology Stack

| Component | Technology |
| --- | --- |
| Language | Python 3.13+ |
| API framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy AsyncIO |
| Database driver | asyncpg |
| Temporary holds | Redis |
| Data validation | Pydantic |
| Configuration | pydantic-settings |
| Authentication | PyJWT |
| Password hashing | pwdlib with Argon2 |
| Database migrations | Alembic |
| Dependency management | uv or pip |

## Project Structure

```text
app/
├── api/
│   └── routers/       # HTTP endpoints
├── core/              # Settings and application exceptions
├── db/                # Database engine and session management
├── models/            # SQLAlchemy models
├── redis/             # Redis client and key helpers
├── repositories/      # Database queries and persistence
├── schemas/           # Request and response models
├── services/          # Business logic and seat holds
├── utils/             # Password hashing and JWT helpers
└── main.py            # FastAPI application entry point

alembic/
├── versions/          # Database migration revisions
└── env.py             # Migration configuration

alembic.ini
pyproject.toml
requirements.txt
uv.lock
```

Requests follow this general flow:

```text
API Router → Service → Repository → PostgreSQL
                 │
                 └── Redis seat holds
```

## Local Development

### Prerequisites

- Python 3.13 or newer
- PostgreSQL
- Redis
- uv, or Python's built-in venv and pip

Run the following commands from the project root.

### 1. Install Dependencies

Using uv:

```bash
uv sync --locked
```

Alternatively, using pip on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```dotenv
DB_CONNECTION=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/<your database name>
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET_EMAIL=....
```

| Variable | Description | Default |
| --- | --- | --- |
| `DB_CONNECTION` | SQLAlchemy asynchronous PostgreSQL connection URL | Required |
| `REDIS_URL` | Redis connection URL | Required |
| `SECRET_KEY` | JWT signing secret | Required |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | `30` |
| `SECRET_EMAIL` | Email address used for administrator authorization | Required |

Generate a signing secret with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Keep real credentials out of version control. The repository's `.env.example` is currently empty.

Administrator authorization compares the authenticated user's email with `SECRET_EMAIL`. This setting does not create an administrator account.

### 3. Prepare the Database

Create the PostgreSQL database referenced by `DB_CONNECTION` and ensure Redis is running.

**The checked-in migration history does not currently initialize an empty database.** Its initial revision creates `bookings` but assumes the referenced `users`, `events`, and `seats` tables already exist. The migration also omits the `expired` booking status used by the application.

Complete or reconcile the migration history before initializing a fresh database. Once the migrations match the intended schema, apply them with:

```bash
uv run alembic upgrade head
```

For an activated pip environment:

```bash
alembic upgrade head
```

Seat records must also be provisioned separately; the application currently provides no seat-creation endpoint or seed script.

### 4. Start the Development Server

Using uv:

```bash
uv run uvicorn app.main:app --reload
```

For an activated pip environment:

```bash
uvicorn app.main:app --reload
```

The default local server address is `http://127.0.0.1:8000`.

| Resource | URL |
| --- | --- |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI schema | http://127.0.0.1:8000/openapi.json |

## Authentication

Register through `POST /api/users/register` using a JSON body:

```json
{
  "email": "user@example.com",
  "password": "replace-with-your-password"
}
```

Request an access token through `POST /api/users/token`.

The token endpoint accepts form-encoded fields, not JSON:

```text
username=user@example.com
password=replace-with-your-password
```

Use the email address as the `username`.

Successful authentication returns:

```json
{
  "access_token": "<jwt-access-token>",
  "token_type": "bearer"
}
```

Include the token in authenticated requests:

```http
Authorization: Bearer <jwt-access-token>
```

In Swagger UI, use **Authorize** to sign in.

## API Reference

### Users

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| POST | `/api/users/register` | Register a user | Public |
| POST | `/api/users/token` | Obtain an access token | Public |
| GET | `/api/users/me` | Retrieve the current user | Authenticated |

### Venues

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/api/venue` | List venues | Public |
| GET | `/api/venue/{venue_id}` | Retrieve a venue | Public |
| POST | `/api/venue` | Create a venue | Administrator |
| DELETE | `/api/venue/{venue_id}` | Delete a venue | Administrator |

### Events

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/api/venue/{venue_id}/events` | List events at a venue | Public |
| GET | `/api/event/{event_id}` | Retrieve an event | Public |
| POST | `/api` | Create an event | Administrator |
| PATCH | `/api/event/{event_id}` | Update an event | Administrator |
| DELETE | `/api/{event_id}` | Delete an event | Administrator |

Event creation and deletion paths above reflect the current implementation. Event PATCH requests currently require a `status` field.

### Seats

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/api/venue/{venue_id}/seats` | List a venue's seats | Public |

The seat listing describes venue seating; it does not report event-specific availability.

### Bookings

| Method | Endpoint | Description | Access |
| --- | --- | --- | --- |
| GET | `/api/booking` | List the current user's bookings | Authenticated |
| GET | `/api/booking/{booking_id}` | Retrieve an owned booking | Authenticated |
| POST | `/api/booking` | Create a temporary booking | Authenticated |
| POST | `/api/booking/{booking_id}/confirm` | Confirm an owned booking | Authenticated |

## Booking Workflow

1. Select an event and a seat belonging to its venue.
2. Submit the identifiers to `POST /api/booking`:

   ```json
   {
     "event_id": 1,
     "seat_id": 12
   }
   ```

3. The service locks the seat row, checks for expired and active bookings, and attempts to acquire a Redis hold.
4. A successful request creates a booking with status `held` and a ten-minute expiry.
5. Confirm the booking through `POST /api/booking/{booking_id}/confirm` before its expiry.

Both the Redis hold duration and database booking duration are configured for ten minutes.

The booking status enum includes:

| Status | Meaning |
| --- | --- |
| `pending` | Model default; normal booking creation explicitly uses `held` |
| `held` | Temporarily reserved |
| `confirmed` | Confirmed through the booking endpoint |
| `expired` | Hold has expired and been processed by application logic |

Database expiry is processed during relevant booking requests. There is no background expiry worker, so elapsed holds may remain labeled `held` until processed.

Confirmation currently simulates successful payment. It does not charge a customer or verify a payment provider transaction.

## Current Limitations

- Booking creation does not enforce event publication status or start time.
- Cancellation, refunds, and real payment integration are not implemented.
- Automated tests are not currently included.


Core scenarios for future coverage include authentication, administrator authorization, concurrent booking attempts, hold expiry, confirmation retries, and migration setup on an empty database.