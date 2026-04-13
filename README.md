# Vedara Agent Console Backend API

A production-ready FastAPI application for the Vedara Agent Console.

## Project Structure

```
├── app/                   # Application package
│   ├── api/              # API routes
│   │   └── routes/       # Endpoint definitions
│   ├── core/             # Core application configuration
│   ├── models/           # Database models
│   ├── schemas/          # Pydantic schemas
│   ├── utils/            # Utility functions
│   ├── middleware/       # Custom middleware
│   └── main.py           # FastAPI app initialization
├── tests/                # Test suite
├── logs/                 # Application logs
├── .env                  # Environment variables
├── .env.example          # Example environment variables
├── requirements.txt      # Python dependencies
└── main.py              # Application entry point
```

## Prerequisites

- Python 3.9+
- pip or conda

## Setup

### 1. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

Update `.env` with your specific configuration:

```env
APP_NAME=Vedara Agent Console API
BASE_URL=http://localhost:8000
DEBUG=True
ENVIRONMENT=development
```

### 4. Run Application

```bash
# Development server with auto-reload
python main.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## Development

### Run Tests

```bash
pytest
```

### Code Quality Checks

```bash
# Format code
black app/ tests/

# Lint
flake8 app/ tests/

# Type checking
mypy app/
```

## Project Features

- ✅ Production-ready folder structure
- ✅ Environment configuration management
- ✅ Middleware support
- ✅ Pydantic schemas for data validation
- ✅ SQLAlchemy ORM setup (optional)
- ✅ Logging configuration
- ✅ CORS support
- ✅ Health check endpoint
- ✅ Testing setup with pytest
- ✅ Code quality tools (black, flake8, mypy)

## Environment Variables

See `.env.example` for all available configuration options:

- `BASE_URL`: Base URL for the API
- `HOST`: Server host
- `PORT`: Server port
- `DEBUG`: Debug mode flag
- `ENVIRONMENT`: Environment (development/staging/production)
- `SECRET_KEY`: Secret key for security
- `LOG_LEVEL`: Logging level
- `LOG_FILE`: Log file path

## Contributing

Follow the project structure and use code quality tools before committing:

```bash
black app/ tests/
flake8 app/ tests/
mypy app/
pytest
```

## License

MIT
