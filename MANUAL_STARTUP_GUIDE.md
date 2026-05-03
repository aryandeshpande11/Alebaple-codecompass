# Manual Startup Guide - Code Onboarding Accelerator

## Current Status
- ✅ Backend code complete
- ✅ Frontend code complete
- ⏳ Frontend dependencies installing (npm install running)

## Step-by-Step Instructions

### Step 1: Wait for npm install to complete

The `npm install` command is currently running in Terminal 1. Wait for it to finish (you'll see "added X packages" message).

### Step 2: Start the Backend Server

Open a **NEW PowerShell terminal** and run:

```powershell
cd c:\Users\hp\OneDrive\Desktop\ibm-hackathon\backend
python -m uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend:**
- Open browser: http://localhost:8000/docs
- You should see the FastAPI Swagger documentation

### Step 3: Start the Frontend Server

Once npm install completes, open **ANOTHER PowerShell terminal** and run:

```powershell
cd c:\Users\hp\OneDrive\Desktop\ibm-hackathon\frontend
npm run dev
```

**Expected Output:**
```
  VITE v5.0.11  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

**Verify Frontend:**
- Open browser: http://localhost:5173
- You should see the professional homepage with IBM branding

### Step 4: Test the Application

1. **Homepage Test:**
   - Visit http://localhost:5173
   - You should see:
     - Hero section with gradient background
     - Upload form
     - Features section
     - How it works section

2. **Backend API Test:**
   - Visit http://localhost:8000/api/v1/health
   - Should return: `{"status": "healthy"}`

3. **Full Integration Test:**
   - On the homepage, enter a GitHub URL: `https://github.com/pallets/flask`
   - Click "Analyze Repository"
   - Wait for analysis to complete
   - View the results in the dashboard

---

## Troubleshooting

### If npm install fails or takes too long:

**Option 1: Cancel and retry**
```powershell
# Press Ctrl+C to cancel
cd frontend
npm cache clean --force
npm install
```

**Option 2: Install specific packages**
```powershell
cd frontend
npm install react react-dom
npm install @carbon/react @carbon/icons-react
npm install axios react-router-dom @monaco-editor/react
npm install -D vite @vitejs/plugin-react
```

### If Backend fails to start:

**Check Python version:**
```powershell
python --version  # Should be 3.10 or higher
```

**Install missing dependencies:**
```powershell
cd backend
pip install fastapi uvicorn pydantic python-multipart
pip install GitPython radon tree-sitter
```

**Check if port 8000 is in use:**
```powershell
# Use a different port
python -m uvicorn app.main:app --reload --port 8001
```

Then update frontend API URL in `frontend/src/services/api.js`:
```javascript
baseURL: 'http://localhost:8001/api/v1'
```

### If Frontend fails to start:

**Check Node.js version:**
```powershell
node --version  # Should be 18 or higher
npm --version
```

**Clear and reinstall:**
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

## Quick Commands Reference

### Backend Commands
```powershell
# Start backend
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Test backend
curl http://localhost:8000/api/v1/health

# View API docs
# Open: http://localhost:8000/docs
```

### Frontend Commands
```powershell
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## What You Should See

### Backend (http://localhost:8000/docs)
- FastAPI Swagger UI
- Multiple API endpoints:
  - `/api/v1/projects` - Project management
  - `/api/v1/projects/{id}/analyze` - Code analysis
  - `/api/v1/ai/explain` - AI explanations
  - And more...

### Frontend (http://localhost:5173)

**Homepage:**
- Professional hero section with blue-purple gradient
- IBM branding in header
- Upload form for GitHub repositories
- 4 feature tiles
- How it works section (4 steps)
- Footer with IBM credits

**After Analysis:**
- Dashboard with metrics (Files, LOC, Functions, Classes)
- Code Explorer tab with file list
- Monaco Editor for code viewing
- AI Insights tab for explanations

---

## Expected Behavior

1. **Upload Repository:**
   - Enter GitHub URL
   - Click "Analyze Repository"
   - Redirected to analysis page
   - See "Analysis in Progress" notification

2. **View Analysis:**
   - Dashboard shows metrics
   - Language statistics displayed
   - Color-coded metric tiles

3. **Explore Code:**
   - Switch to "Code Explorer" tab
   - Click on files to view code
   - Syntax highlighting works
   - Click "Explain with AI" for insights

4. **AI Insights:**
   - Switch to "AI Insights" tab
   - See AI-generated explanations
   - View key points, complexity, suggestions

---

## System Requirements

- **Python:** 3.10 or higher
- **Node.js:** 18 or higher
- **npm:** 9 or higher
- **Git:** Latest version
- **OS:** Windows 11 (PowerShell)
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 2GB free space

---

## Port Usage

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs

Make sure these ports are not in use by other applications.

---

## Next Steps After Startup

1. Test the upload functionality
2. Analyze a sample repository
3. Explore the code viewer
4. Test AI explanations
5. Check responsive design (resize browser)
6. Test theme toggle (light/dark)

---

## Support

If you encounter any issues:

1. Check the terminal output for error messages
2. Verify all dependencies are installed
3. Ensure ports 8000 and 5173 are available
4. Check the troubleshooting section above
5. Review the logs in the terminal

---

**Status:** Ready for testing once npm install completes!

_Made with Bob - Enterprise Edition_