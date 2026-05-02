# Setup Guide - Code Understanding and Onboarding Accelerator

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher (for frontend, coming soon)
- Git

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Development Server

```bash
# Option 1: Using uvicorn directly
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using the main.py file
python app/main.py
```

### 6. Test the API

Open your browser and visit:

- **API Root (Hello World)**: http://localhost:8000/
- **API Documentation (Swagger UI)**: http://localhost:8000/api/docs
- **API Documentation (ReDoc)**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/api/health
- **API Info**: http://localhost:8000/api/v1/info

You should see a JSON response with "Hello World!" message.

## Project Structure

```
ibm-hackathon/
├── .gitignore                    # Git ignore rules
├── README.md                     # Project overview
├── SETUP.md                      # This file
├── tech-stack-plan.md           # Technical architecture plan
├── backend/                      # Backend application
│   ├── README.md                # Backend documentation
│   ├── requirements.txt         # Python dependencies
│   ├── venv/                    # Virtual environment (not in git)
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI application entry point
│       ├── api/
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       └── endpoints/   # API endpoint modules
│       ├── core/                # Core configurations
│       ├── models/              # Database models
│       ├── schemas/             # Pydantic schemas
│       ├── services/            # Business logic
│       └── utils/               # Utility functions
└── frontend/                     # Frontend application (coming soon)
    ├── README.md
    └── src/
        ├── components/
        ├── pages/
        ├── services/
        ├── utils/
        └── assets/
```

## Available API Endpoints

### Root Endpoints

- `GET /` - Hello World endpoint
  ```json
  {
    "message": "Hello World! Welcome to Code Understanding and Onboarding Accelerator API",
    "status": "running",
    "version": "0.1.0"
  }
  ```

- `GET /api/health` - Health check endpoint
  ```json
  {
    "status": "healthy",
    "service": "Code Understanding and Onboarding Accelerator"
  }
  ```

- `GET /api/v1/info` - API information
  ```json
  {
    "api_name": "Code Understanding and Onboarding Accelerator",
    "version": "0.1.0",
    "endpoints": {
      "root": "/",
      "health": "/api/health",
      "docs": "/api/docs",
      "redoc": "/api/redoc"
    }
  }
  ```

## Development Workflow

1. **Make changes** to the code
2. **Server auto-reloads** (when using `--reload` flag)
3. **Test endpoints** using the Swagger UI at http://localhost:8000/api/docs
4. **Commit changes** to Git

## Troubleshooting

### Virtual Environment Issues

If you have issues activating the virtual environment:

**Windows PowerShell Execution Policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use

If port 8000 is already in use, change the port:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Module Not Found Errors

Make sure you:
1. Activated the virtual environment
2. Installed all dependencies: `pip install -r requirements.txt`
3. Are in the correct directory

## Next Steps

1. ✅ Backend structure created
2. ✅ FastAPI Hello World working
3. ⏳ Add database configuration
4. ⏳ Implement authentication
5. ⏳ Add code analysis endpoints
6. ⏳ Integrate watsonx.ai
7. ⏳ Add watsonx Orchestrate workflows
8. ⏳ Build React frontend

## Support

For issues or questions, refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- Project tech stack plan: `tech-stack-plan.md`