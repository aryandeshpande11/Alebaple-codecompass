# Quick Setup Commands - Execute in Order

## Backend Setup (Execute these commands)

### Step 1: Navigate to backend directory
```bash
cd backend
```

### Step 2: Create Python virtual environment
```bash
python -m venv venv
```

### Step 3: Activate virtual environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Step 5: Install all dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Install additional hackathon dependencies
```bash
pip install GitPython==3.1.40 radon==6.0.1 pylint==3.0.3 ibm-watsonx-ai==0.2.6 redis==5.0.1 celery==5.3.4 sqlalchemy==2.0.23 alembic==1.13.0 requests==2.31.0
```

### Step 7: Verify installation
```bash
pip list
```

### Step 8: Run the FastAPI server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 9: Test the API (open in browser)
- http://localhost:8000/
- http://localhost:8000/api/docs
- http://localhost:8000/api/health

---

## Frontend Setup (Execute after backend is running)

### Step 1: Open new terminal and navigate to frontend
```bash
cd frontend
```

### Step 2: Initialize React app with Vite
```bash
npm create vite@latest . -- --template react
```

### Step 3: Install dependencies
```bash
npm install
```

### Step 4: Install Carbon Design System
```bash
npm install @carbon/react @carbon/icons-react
```

### Step 5: Install additional dependencies
```bash
npm install axios react-router-dom @monaco-editor/react react-query mermaid
```

### Step 6: Run development server
```bash
npm run dev
```

### Step 7: Test frontend (open in browser)
- http://localhost:5173/

---

## Complete Requirements.txt for Backend

If you need to update `backend/requirements.txt` with all dependencies:

```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
python-dotenv==1.0.0

# Code Analysis
GitPython==3.1.40
radon==6.0.1
pylint==3.0.3

# AI Integration
ibm-watsonx-ai==0.2.6

# Database & Caching
sqlalchemy==2.0.23
alembic==1.13.0
redis==5.0.1

# Task Queue
celery==5.3.4

# Utilities
requests==2.31.0
```

---

## Verification Commands

### Check Python version
```bash
python --version
```
Should show: Python 3.10 or higher

### Check Node version
```bash
node --version
```
Should show: v18.0.0 or higher

### Check npm version
```bash
npm --version
```

### Check if virtual environment is activated
```bash
which python
# or on Windows:
where python
```
Should point to the venv directory

### List installed Python packages
```bash
pip list
```

### Check if FastAPI is running
```bash
curl http://localhost:8000/api/health
```

---

## Quick Start (All-in-One)

### Backend (PowerShell - Windows)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install GitPython==3.1.40 radon==6.0.1 pylint==3.0.3 ibm-watsonx-ai==0.2.6 redis==5.0.1 celery==5.3.4 sqlalchemy==2.0.23 alembic==1.13.0 requests==2.31.0
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Backend (Bash - macOS/Linux)
```bash
cd backend && \
python -m venv venv && \
source venv/bin/activate && \
python -m pip install --upgrade pip && \
pip install -r requirements.txt && \
pip install GitPython==3.1.40 radon==6.0.1 pylint==3.0.3 ibm-watsonx-ai==0.2.6 redis==5.0.1 celery==5.3.4 sqlalchemy==2.0.23 alembic==1.13.0 requests==2.31.0 && \
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (New Terminal)
```bash
cd frontend && \
npm create vite@latest . -- --template react && \
npm install && \
npm install @carbon/react @carbon/icons-react axios react-router-dom @monaco-editor/react react-query mermaid && \
npm run dev
```

---

## Troubleshooting

### PowerShell Execution Policy Error
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 8000 Already in Use
```bash
# Use different port
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Module Not Found
```bash
# Make sure venv is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Port Conflict
```bash
# Vite will automatically use next available port (5174, 5175, etc.)
```

---

## Environment Variables Setup

Create `.env` file in backend directory:

```bash
cd backend
```

Create file `backend/.env`:
```env
# Database
DATABASE_URL=postgresql://dev:dev@localhost:5432/code_accelerator

# Redis
REDIS_URL=redis://localhost:6379

# watsonx.ai
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Cloud
IBM_CLOUD_API_KEY=your_cloud_api_key_here

# Security
JWT_SECRET=your_secret_key_here_change_in_production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Code Understanding and Onboarding Accelerator
APP_VERSION=0.1.0
DEBUG=True
```

---

## Success Indicators

✅ Virtual environment created and activated  
✅ All Python packages installed without errors  
✅ FastAPI server running on http://localhost:8000  
✅ API docs accessible at http://localhost:8000/api/docs  
✅ Health check returns {"status": "healthy"}  
✅ Frontend dev server running on http://localhost:5173  
✅ No error messages in terminal  

---

## Next Steps After Setup

1. Test all API endpoints in Swagger UI
2. Start implementing code analysis features
3. Integrate watsonx.ai
4. Build React components
5. Connect frontend to backend
6. Prepare demo repository
