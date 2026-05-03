"""
Main FastAPI application entry point
Code Understanding and Onboarding Accelerator
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
import time
import logging

from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="Code Understanding and Onboarding Accelerator API",
    description="API for analyzing code repositories and generating onboarding materials with IBM watsonx.ai",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {process_time:.3f}s")
    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "type": type(exc).__name__
        }
    )

# Include API v1 router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint - Hello World"""
    return {
        "message": "Welcome to Code Understanding and Onboarding Accelerator API",
        "status": "running",
        "version": "0.2.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Code Understanding and Onboarding Accelerator",
        "version": "0.2.0"
    }


@app.get("/api/v1/info")
async def api_info():
    """API information endpoint"""
    return {
        "api_name": "Code Understanding and Onboarding Accelerator",
        "version": "0.3.0",
        "endpoints": {
            "root": "/",
            "health": "/api/health",
            "docs": "/api/docs",
            "redoc": "/api/redoc",
            "projects": "/api/v1/projects",
            "analysis": "/api/v1/projects/{project_id}/analyze",
            "ai_analysis": "/api/v1/projects/{project_id}/analyze-with-ai",
            "ai_explain": "/api/v1/ai/explain",
            "ai_summarize": "/api/v1/ai/summarize",
            "ai_document": "/api/v1/ai/document",
            "ai_health": "/api/v1/ai/health"
        },
        "features": [
            "Project management",
            "Multi-language code analysis (Python, Java, JavaScript, TypeScript)",
            "IBM watsonx.ai integration for code explanation",
            "AI-powered code documentation generation",
            "Intelligent code summarization",
            "Response caching for improved performance",
            "Enhanced analysis with AI insights"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
