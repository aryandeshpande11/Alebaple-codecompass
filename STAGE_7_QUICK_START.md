# Stage 7: Quick Start Guide

## 🚀 One-Command Demo Startup

### Windows (Recommended)
```powershell
.\start_demo.ps1
```

### Windows (Alternative)
```cmd
start_demo.bat
```

This will:
1. ✅ Validate environment setup
2. ✅ Start backend server (port 8000)
3. ✅ Start frontend server (port 5173)
4. ✅ Open browser automatically

---

## 🧪 Run Tests

### End-to-End Tests
```bash
cd backend
python test_stage7_e2e.py
```

**Note:** Backend must be running for tests to pass.

---

## 🔧 Manual Startup (If Needed)

### Terminal 1: Backend
```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

### Terminal 3: Tests (Optional)
```bash
cd backend
python test_stage7_e2e.py
```

---

## 🌐 Access Points

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/api/health

---

## ✅ Pre-Demo Checklist

- [ ] Backend .env file configured with watsonx.ai credentials
- [ ] Both servers running without errors
- [ ] Browser opens to frontend
- [ ] Demo repository URL ready
- [ ] Review STAGE_7_DEMO_SCRIPT.md

---

## 🎯 Stage 7 Deliverables

### Code Enhancements
1. ✅ **test_stage7_e2e.py** - Comprehensive E2E test suite
2. ✅ **start_demo.ps1** - PowerShell startup script
3. ✅ **start_demo.bat** - Batch startup script
4. ✅ **Enhanced main.py** - Logging, compression, error handling
5. ✅ **PerformanceMonitor** - Real-time performance tracking

### Documentation
1. ✅ **STAGE_7_COMPLETION_REPORT.md** - Full completion report
2. ✅ **STAGE_7_DEMO_SCRIPT.md** - Complete demo guide
3. ✅ **STAGE_7_QUICK_START.md** - This file

---

## 🎉 Status: STAGE 7 COMPLETE

**Ready for:**
- ✅ Live demonstrations
- ✅ User testing  
- ✅ Production deployment
- ✅ Stakeholder presentations

---

Made with ❤️ by Bob