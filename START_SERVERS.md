# Starting the Application

## Quick Start Guide

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ installed
- Git installed

### Step 1: Install Backend Dependencies

Open a terminal and run:

```powershell
cd backend
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

Open another terminal and run:

```powershell
cd frontend
npm install
```

### Step 3: Start Backend Server

In the backend terminal:

```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Backend will be available at: **http://localhost:8000**
API Documentation: **http://localhost:8000/docs**

### Step 4: Start Frontend Server

In the frontend terminal:

```powershell
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:5173**

---

## PowerShell Script (Alternative)

You can also use these PowerShell commands:

### Start Backend:
```powershell
cd c:\Users\hp\OneDrive\Desktop\ibm-hackathon\backend
python -m uvicorn app.main:app --reload --port 8000
```

### Start Frontend (in new terminal):
```powershell
cd c:\Users\hp\OneDrive\Desktop\ibm-hackathon\frontend
npm run dev
```

---

## Verification

1. **Backend Health Check**: Visit http://localhost:8000/api/v1/health
2. **Frontend**: Visit http://localhost:5173
3. **API Docs**: Visit http://localhost:8000/docs

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```powershell
# Use a different port
python -m uvicorn app.main:app --reload --port 8001
```

**Missing dependencies:**
```powershell
pip install fastapi uvicorn pydantic python-multipart GitPython radon tree-sitter
```

### Frontend Issues

**Port already in use:**
- Vite will automatically try the next available port (5174, 5175, etc.)

**Missing dependencies:**
```powershell
npm install
```

**Build errors:**
```powershell
# Clear cache and reinstall
rm -r node_modules
rm package-lock.json
npm install
```

---

## Testing the Integration

1. Start both servers
2. Open http://localhost:5173 in your browser
3. Enter a GitHub repository URL (e.g., `https://github.com/pallets/flask`)
4. Click "Analyze Repository"
5. View the analysis results

---

## Stopping the Servers

- Press `Ctrl+C` in each terminal to stop the servers

---

_Made with Bob - Enterprise Edition_