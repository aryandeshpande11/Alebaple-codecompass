"""
Main FastAPI application entry point
Code Understanding and Onboarding Accelerator
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI(
    title="Code Understanding and Onboarding Accelerator API",
    description="API for analyzing code repositories and generating onboarding materials",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - Hello World"""
    return {
        "message": "Hello World! Welcome to Code Understanding and Onboarding Accelerator API",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Code Understanding and Onboarding Accelerator"
    }


@app.get("/api/v1/info")
async def api_info():
    """API information endpoint"""
    return {
        "api_name": "Code Understanding and Onboarding Accelerator",
        "version": "0.1.0",
        "endpoints": {
            "root": "/",
            "health": "/api/health",
            "docs": "/api/docs",
            "redoc": "/api/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
