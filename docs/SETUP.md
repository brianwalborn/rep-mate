# Setup Guide

Get Rep Mate up and running on your local machine with Docker in under 5 minutes.

## Prerequisites

- [Docker Desktop](https://docs.docker.com/get-docker/) installed and running
- Git (to clone the repository)

## Quick Start

### 1. Clone and Navigate

```bash
git clone https://github.com/brianwalborn/rep-mate.git
cd rep-mate
```

### 2. Start Everything

```bash
docker-compose up --build
```

This single command will:
- Build the frontend and backend Docker images
- Start a PostgreSQL database
- Run database migrations automatically
- Launch the FastAPI backend server on port 8000
- Launch the Vue.js frontend on port 5173

### 3. Access the App

Open your browser to:

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/health

Create an account and start tracking your workouts! 💪

### 4. Stop the App

```bash
docker-compose down
```

To remove all data including the database:

```bash
docker-compose down -v
```

## Database Management

### Access the Database Console

```bash
docker-compose exec database psql -U repmate -d repmate
```

### Run Migrations

After modifying database models:

```bash
docker-compose exec backend alembic revision --autogenerate -m "your_migration_name"
docker-compose exec backend alembic upgrade head
```

## Configuration

### Default Database Credentials

Defined in `docker-compose.yml`:
- **Username**: `repmate`
- **Password**: `password`
- **Database**: `repmate`
- **Port**: `5432`

⚠️ **Important**: Change these before deploying to production!

### Environment Variables (Optional)

Create `frontend/.env` to customize:

```env
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Port Conflicts

If ports 5173, 8000, or 5432 are already in use, modify `docker-compose.yml`:

```yaml
services:
  frontend:
    ports:
      - "5174:80"  # change 5173 → 5174

  backend:
    ports:
      - "8001:8000"  # change 8000 → 8001

  database:
    ports:
      - "5433:5432"  # change 5432 → 5433
```

### Containers Won't Start

1. Ensure Docker Desktop is running
2. Check for port conflicts (see above)
3. Try rebuilding: `docker-compose up --build --force-recreate`

### Database Connection Issues

The `docker-compose.yml` includes health checks to ensure the database is ready before the backend starts. If you still see connection errors, wait a few seconds and refresh.

### Migration Errors

1. Check that all model changes are saved
2. Verify model imports in `backend/alembic/env.py`
3. Review migration files in `backend/alembic/versions/`
4. If needed, reset the database: `docker-compose down -v` then `docker-compose up --build`

## Support

Need help? Open an issue on [GitHub](https://github.com/brianwalborn/rep-mate/issues).
