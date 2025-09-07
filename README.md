# Atmanaut

Smart AI-powered journaling app with mood tracking & analytics.

## Stack
- Backend: FastAPI + Supabase
- Frontend: Next.js + React + TypeScript
- DB: PostgreSQL (Supabase)
- Auth: Clerk JWT
- External APIs: AdviceSlip (daily prompts)

## Core Features
Users:
- Smart mood-based journaling
- AI-generated mood images
- Collection organization
- Analytics & insights
- Daily writing prompts

System:
- JWT authentication with Clerk
- Rate limiting & security
- Real-time analytics
- Responsive design

## Environment (.env)
Backend (.env in backend-python/):
```
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Clerk Authentication
CLERK_SECRET_KEY=your_clerk_secret_key
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key

# External APIs
PIXABAY_API_KEY=your_pixabay_api_key

# App Settings
DEBUG=true
APP_NAME=Atmanaut
```

Frontend (.env.local):
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Quick Start
Backend:
```bash
cd backend-python
poetry install
cp .env.example .env  # fill values
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd /path/to/atmanaut
npm install
npm run dev
```

Development (both):
```bash
./start-dev.sh  # starts both backend and frontend
```

URLs:
- App: http://localhost:3000
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## API Endpoints
Authentication required for all endpoints except `/public/*`

Journals:
```
GET    /journal/entries                    # Get all entries
GET    /journal/entries/collection/{id}    # Get entries by collection
GET    /journal/entries/{id}              # Get specific entry
POST   /journal/                          # Create entry
PUT    /journal/entries/{id}              # Update entry
DELETE /journal/entries/{id}              # Delete entry
```

Collections:
```
GET    /collections/                      # Get all collections
POST   /collections/                      # Create collection
PUT    /collections/{id}                  # Update collection
DELETE /collections/{id}                  # Delete collection
```

Analytics:
```
GET    /analytics/?period=30d             # Get mood analytics
```

Public:
```
GET    /public/daily-prompt               # Get daily writing prompt
```

## Example Usage
Create a journal entry:
```bash
curl -X POST http://localhost:8000/journal/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Great Day!",
    "content": "<p>Had an amazing day today!</p>",
    "mood": "happy",
    "moodQuery": "sunny day happiness"
  }'
```

Get analytics:
```bash
curl -X GET "http://localhost:8000/analytics/?period=7d" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Development Tools
Testing mode (no auth):
```bash
./switch-mode.sh test    # Switch to testing mode
./switch-mode.sh prod    # Switch back to production
```

## Database Schema
Tables managed by Supabase:
- `users` - User profiles from Clerk
- `entries` - Journal entries with mood data
- `collections` - Entry collections/categories

## Mood System
Built-in moods with scores (1-10):
- Radiant (10), Ecstatic (9), Overjoyed (8)
- Happy (7), Good (6), Okay (5)
- Meh (4), Anxious (3), Sad (2), Devastated (1)

Each mood includes:
- Emoji representation
- Color theme
- Writing prompt
- Pixabay search query for images

## Troubleshooting
**Auth errors**: Check Clerk keys in environment files
**CORS issues**: Verify API_URL in frontend .env.local
**Database errors**: Check Supabase connection & permissions
**Image loading**: Verify Pixabay API key
**Rate limiting**: Check Redis connection (optional)

