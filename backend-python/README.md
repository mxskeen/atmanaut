# Atmanaut FastAPI Backend

A Python FastAPI backend for the Atmanaut journaling application, migrated from the original JavaScript/Next.js backend.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **Supabase** - Backend-as-a-Service with PostgreSQL database
- **Poetry** - Dependency management
- **Clerk Authentication** - User authentication and management
- **Rate Limiting** - API rate limiting with SlowAPI (in-memory)
- **External APIs** - Integration with AdviceSlip API

## Setup

### Prerequisites

- Python 3.11+
- Poetry

### Installation

1. Clone the repository and navigate to the backend directory:

```bash
cd backend-python
```

2. Install dependencies with Poetry:

```bash
poetry install
```

3. Copy environment file and configure:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Set up the database:

```bash
# Run database setup script
./migrate.sh
```

5. Start the development server:

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend-python/
├── app/
│   ├── core/           # Core configuration and settings
│   ├── schemas/        # Pydantic schemas
│   ├── routers/        # API route handlers
│   ├── services/       # Business logic and Supabase integration
│   ├── middleware/     # Custom middleware
│   └── main.py         # FastAPI application setup
├── pyproject.toml      # Poetry configuration
├── migrate.sh          # Database setup script
└── README.md          # This file
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Clerk Authentication
CLERK_SECRET_KEY=your_clerk_secret_key_here
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key_here

# External APIs


# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]

# Rate limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=3600

# Debug
DEBUG=true
```

## API Endpoints

### Analytics

- `GET /analytics/` - Get user analytics data

### Collections

- `GET /collections/` - Get user collections
- `POST /collections/` - Create new collection
- `PUT /collections/{id}` - Update collection
- `DELETE /collections/{id}` - Delete collection

### Journal Entries

- `GET /journal/entries` - Get journal entries
- `POST /journal/entries` - Create new entry
- `GET /journal/entries/{id}` - Get specific entry
- `PUT /journal/entries/{id}` - Update entry
- `DELETE /journal/entries/{id}` - Delete entry

### Drafts

- `GET /journal/draft` - Get current draft
- `POST /journal/draft` - Save draft

### Public

- `GET /public/daily-prompt` - Get daily writing prompt
- `GET /public/mood-image/{mood}` - Get mood-based image

## Authentication

This backend uses Clerk for authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Database Migrations

To set up the database schema in Supabase:

```bash
./migrate.sh
```

This script will create the necessary tables in your Supabase database.

## Development

### Running Tests

```bash
poetry run pytest
```

### Linting

```bash
poetry run black .
poetry run isort .
poetry run flake8
```

## Deployment

For production deployment, consider:

1. Set `DEBUG=false` in environment
2. Use a production ASGI server like Gunicorn with Uvicorn workers
3. Set up proper logging
4. Configure reverse proxy (nginx)
5. Set up SSL certificates
6. Configure Supabase for production use

## Migration from JavaScript Backend

This FastAPI backend replaces the original JavaScript backend with equivalent functionality:

- **Prisma ORM → Supabase REST API**
- **Next.js API routes → FastAPI routers**
- **Clerk middleware → Custom auth middleware**
- **Arcjet rate limiting → SlowAPI (in-memory)**
- **Server actions → Service classes**

All endpoints maintain the same functionality and similar response formats for seamless frontend integration.
