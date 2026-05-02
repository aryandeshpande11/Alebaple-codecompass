"""
Main FastAPI application entry point
Code Understanding and Onboarding Accelerator
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router

# Create FastAPI app instance
app = FastAPI(
    title="Code Understanding and Onboarding Accelerator API",
    description="API for analyzing code repositories and generating onboarding materials",
    version="0.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
