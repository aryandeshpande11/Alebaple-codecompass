# Code Understanding and Onboarding Accelerator - Backend

FastAPI backend for analyzing code repositories and generating onboarding materials.

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
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

### 3. Run the Server

```bash
# From backend directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:

```bash
python app/main.py
```

### 4. Access the API

- **API Root**: http://localhost:8000/
- **API Documentation (Swagger)**: http://localhost:8000/api/docs
- **API Documentation (ReDoc)**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/api/health

## Available Endpoints

- `GET /` - Hello World endpoint
- `GET /api/health` - Health check
- `GET /api/v1/info` - API information

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/   # API endpoint modules
│   ├── core/                # Core configurations
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── requirements.txt
└── README.md
```

## Development

The server runs with auto-reload enabled in development mode. Any changes to the code will automatically restart the server.

## Next Steps

1. Add database configuration
2. Implement authentication
3. Add code analysis endpoints
4. Integrate watsonx.ai
5. Add watsonx Orchestrate workflows