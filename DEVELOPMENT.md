# FastAPI Application Development Guide

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run application
python main.py
```

Visit: http://localhost:8000

### 2. API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

## Project Structure

```
app/
├── api/
│   ├── routes/              # Endpoint implementations
│   │   ├── __init__.py
│   │   ├── health.py       # Health check
│   │   └── users.py        # (Add your endpoints)
│   └── __init__.py         # Router aggregation
├── core/
│   ├── config.py           # Settings from .env
│   ├── constants.py        # App constants
│   └── __init__.py
├── models/
│   ├── base.py             # SQLAlchemy models
│   └── __init__.py
├── schemas/
│   ├── __init__.py         # Pydantic schemas
│   └── base.py             # Common schemas
├── utils/
│   ├── logger.py           # Logging setup
│   └── __init__.py
├── middleware/
│   └── __init__.py
├── main.py                 # FastAPI app factory
└── __init__.py

tests/
├── __init__.py
├── conftest.py            # Pytest configuration
└── test_health.py         # Example tests

Configuration Files:
├── main.py                # Entry point
├── .env                   # Environment variables (local)
├── .env.example           # Template
├── .env.dev              # Development overrides
├── .env.prod             # Production overrides
├── requirements.txt       # Dependencies
├── pyproject.toml        # Project metadata
├── pytest.ini            # Pytest config
├── Dockerfile            # Docker image
├── docker-compose.yml    # Docker services
├── Makefile              # Common commands
└── .pre-commit-config.yaml  # Code quality hooks
```

## Adding New Endpoints

### 1. Create Route Module

Create `app/api/routes/example.py`:

```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/examples", tags=["Examples"])

class Example(BaseModel):
    id: int
    name: str
    description: str

@router.get("", response_model=list[Example])
async def list_examples():
    return []

@router.post("", response_model=Example, status_code=status.HTTP_201_CREATED)
async def create_example(data: Example):
    return data

@router.get("/{example_id}", response_model=Example)
async def get_example(example_id: int):
    return Example(id=example_id, name="Example", description="Test")

@router.put("/{example_id}", response_model=Example)
async def update_example(example_id: int, data: Example):
    return data

@router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(example_id: int):
    pass
```

### 2. Register Route

Update `app/api/__init__.py`:

```python
from app.api.routes import health, example
from app.core.constants import API_V1_PREFIX

api_v1_router = APIRouter(prefix=API_V1_PREFIX)

api_v1_router.include_router(health.router)
api_v1_router.include_router(example.router)
```

## Database Setup (Optional)

### 1. Install Database Driver

```bash
pip install psycopg2-binary sqlalchemy
```

### 2. Update .env

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 3. Create Models

Edit `app/models/base.py`:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
```

## Using Docker

### Start Services

```bash
docker-compose up -d
```

Services:
- API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Stop Services

```bash
docker-compose down
```

## Code Quality

### Format Code

```bash
black app tests
isort app tests
```

### Lint Code

```bash
flake8 app tests
```

### Type Check

```bash
mypy app
```

### Run Tests

```bash
pytest tests/ -v
```

### Using Makefile

```bash
make install    # Install dependencies
make dev        # Run dev server
make test       # Run tests
make lint       # Lint code
make format     # Format code
make clean      # Clean cache
make docker-up  # Start Docker
make docker-down # Stop Docker
```

## Environment Variables

### Required

- `BASE_URL`: Base URL of your API
- `SECRET_KEY`: Secret key for JWT (change in production)

### Optional

- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)
- `DATABASE_URL`: Database connection string
- `ALLOWED_ORIGINS`: CORS allowed origins

See `.env.example` for all options.

## Deployment

### Production Checklist

1. Set `DEBUG=False`
2. Update `SECRET_KEY` to a strong random value
3. Set `ENVIRONMENT=production`
4. Configure `ALLOWED_ORIGINS` with your domain
5. Use a production database (PostgreSQL recommended)
6. Enable HTTPS
7. Set up proper logging
8. Use a production ASGI server (Gunicorn + Uvicorn)

### Production Command

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Or using Docker:

```bash
docker build -t vedara-api .
docker run -p 8000:8000 --env-file .env.prod vedara-api
```

## Troubleshooting

### Import Errors

Ensure you're in the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### Port Already in Use

Change port in `.env`:
```env
PORT=8001
```

### Database Connection Issues

Check your connection string:
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pytest Docs](https://docs.pytest.org/)
