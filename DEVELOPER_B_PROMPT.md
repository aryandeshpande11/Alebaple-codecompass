# Developer B: AI API Endpoints & Caching - Detailed Instructions

## 🎯 Your Mission
Create REST API endpoints for AI-powered code explanation features and implement a caching system to optimize API usage.

---

## 📦 Prerequisites

1. **Pull Latest Code**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/stage4-ai-endpoints
   ```

2. **Wait for Developer A**
   - Developer A will create the core AI service first
   - You can start with mock responses and integrate later
   - Coordinate in team chat when AI service is ready

---

## 📝 Task 1: Create AI Request/Response Schemas

**File:** `backend/app/schemas/ai.py`

```python
"""
Pydantic schemas for AI-powered code explanation features.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class ExplainCodeRequest(BaseModel):
    """Request to explain a code snippet."""
    code: str = Field(..., description="Code snippet to explain")
    language: str = Field(..., description="Programming language (python, java, javascript, typescript)")
    context: Optional[str] = Field(None, description="Additional context about the code")


class ExplainCodeResponse(BaseModel):
    """Response with code explanation."""
    explanation: str = Field(..., description="Human-readable explanation of the code")
    key_concepts: List[str] = Field(default_factory=list, description="Key programming concepts used")
    complexity_note: Optional[str] = Field(None, description="Note about code complexity")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    cached: bool = Field(False, description="Whether response was served from cache")


class ExplainFileRequest(BaseModel):
    """Request to explain an entire file."""
    project_id: str = Field(..., description="Project identifier")
    file_path: str = Field(..., description="Path to file within project")


class SummarizeRequest(BaseModel):
    """Request to summarize code."""
    code: str = Field(..., description="Code to summarize")
    language: str = Field(..., description="Programming language")
    summary_type: str = Field("brief", description="Type of summary: brief, detailed, or technical")


class SummarizeResponse(BaseModel):
    """Response with code summary."""
    summary: str = Field(..., description="Code summary")
    main_purpose: str = Field(..., description="Main purpose of the code")
    key_functions: List[str] = Field(default_factory=list, description="Key functions/methods")
    dependencies: List[str] = Field(default_factory=list, description="Main dependencies")
    cached: bool = Field(False, description="Whether response was served from cache")


class GenerateDocsRequest(BaseModel):
    """Request to generate documentation."""
    code: str = Field(..., description="Code to document")
    language: str = Field(..., description="Programming language")
    doc_style: str = Field("google", description="Documentation style: google, numpy, or sphinx")


class GenerateDocsResponse(BaseModel):
    """Response with generated documentation."""
    documentation: str = Field(..., description="Generated documentation")
    format: str = Field(..., description="Documentation format used")
    cached: bool = Field(False, description="Whether response was served from cache")
```

**Action Items:**
- [ ] Create the file with all schemas
- [ ] Add proper type hints and descriptions
- [ ] Test schema validation with sample data

---

## 📝 Task 2: Implement Caching System

**File:** `backend/app/utils/cache.py`

```python
"""
Simple file-based caching system for AI responses.
"""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any


class AIResponseCache:
    """Cache for AI-generated responses."""
    
    def __init__(self, cache_dir: str = "backend/data/cache"):
        """Initialize cache with directory."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.expiration_hours = 24
    
    def _generate_key(self, code: str, language: str, prompt_type: str) -> str:
        """Generate cache key from inputs."""
        content = f"{code}|{language}|{prompt_type}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, code: str, language: str, prompt_type: str) -> Optional[dict]:
        """Get cached response if available and not expired."""
        key = self._generate_key(code, language, prompt_type)
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check expiration
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.utcnow() - cached_time > timedelta(hours=self.expiration_hours):
                cache_file.unlink()  # Delete expired cache
                return None
            
            return cached_data['response']
        except Exception:
            return None
    
    def set(self, code: str, language: str, prompt_type: str, response: dict) -> None:
        """Cache a response."""
        key = self._generate_key(code, language, prompt_type)
        cache_file = self.cache_dir / f"{key}.json"
        
        cache_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'language': language,
            'prompt_type': prompt_type,
            'response': response
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except Exception:
            pass  # Fail silently on cache errors
    
    def clear_expired(self) -> int:
        """Clear all expired cache entries. Returns count of deleted entries."""
        deleted = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cached_data['timestamp'])
                if datetime.utcnow() - cached_time > timedelta(hours=self.expiration_hours):
                    cache_file.unlink()
                    deleted += 1
            except Exception:
                continue
        
        return deleted
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'total_entries': len(cache_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'cache_dir': str(self.cache_dir)
        }


# Global cache instance
ai_cache = AIResponseCache()
```

**Action Items:**
- [ ] Create the cache utility
- [ ] Create `backend/data/cache/` directory
- [ ] Test caching with sample data
- [ ] Verify expiration logic works

---

## 📝 Task 3: Create AI API Endpoints

**File:** `backend/app/api/v1/endpoints/ai.py`

```python
"""
AI-powered code explanation API endpoints.
"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.ai import (
    ExplainCodeRequest,
    ExplainCodeResponse,
    ExplainFileRequest,
    SummarizeRequest,
    SummarizeResponse,
    GenerateDocsRequest,
    GenerateDocsResponse
)
from app.utils.cache import ai_cache
from app.utils.storage import storage

router = APIRouter()

# TODO: Import AI service when Developer A completes it
# from app.services.ai_service import ai_service


@router.post("/explain", response_model=ExplainCodeResponse)
async def explain_code(request: ExplainCodeRequest):
    """
    Explain a code snippet using AI.
    
    - **code**: The code snippet to explain
    - **language**: Programming language (python, java, javascript, typescript)
    - **context**: Optional context about the code
    """
    # Check cache first
    cached_response = ai_cache.get(request.code, request.language, "explain")
    if cached_response:
        cached_response['cached'] = True
        return ExplainCodeResponse(**cached_response)
    
    try:
        # TODO: Replace with actual AI service call
        # explanation = ai_service.explain_code(request.code, request.language)
        
        # Mock response for now
        response_data = {
            "explanation": f"This {request.language} code performs specific operations...",
            "key_concepts": ["variables", "functions", "control flow"],
            "complexity_note": "Moderate complexity",
            "suggestions": ["Consider adding error handling", "Add documentation"],
            "cached": False
        }
        
        # Cache the response
        ai_cache.set(request.code, request.language, "explain", response_data)
        
        return ExplainCodeResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain code: {str(e)}"
        )


@router.post("/explain-file", response_model=ExplainCodeResponse)
async def explain_file(request: ExplainFileRequest):
    """
    Explain an entire file from a project.
    
    - **project_id**: Project identifier
    - **file_path**: Path to file within project
    """
    # Get project
    project = storage.get_project(request.project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{request.project_id}' not found"
        )
    
    # TODO: Get file content from repository
    # For now, return mock response
    
    try:
        response_data = {
            "explanation": f"This file contains implementation for...",
            "key_concepts": ["classes", "methods", "imports"],
            "complexity_note": "Well-structured code",
            "suggestions": ["Good code organization"],
            "cached": False
        }
        
        return ExplainCodeResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain file: {str(e)}"
        )


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_code(request: SummarizeRequest):
    """
    Generate a summary of code.
    
    - **code**: Code to summarize
    - **language**: Programming language
    - **summary_type**: Type of summary (brief, detailed, technical)
    """
    # Check cache
    cached_response = ai_cache.get(request.code, request.language, f"summarize_{request.summary_type}")
    if cached_response:
        cached_response['cached'] = True
        return SummarizeResponse(**cached_response)
    
    try:
        # TODO: Replace with actual AI service call
        response_data = {
            "summary": f"This code implements...",
            "main_purpose": "Primary functionality description",
            "key_functions": ["function1", "function2"],
            "dependencies": ["library1", "library2"],
            "cached": False
        }
        
        # Cache the response
        ai_cache.set(request.code, request.language, f"summarize_{request.summary_type}", response_data)
        
        return SummarizeResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarize code: {str(e)}"
        )


@router.post("/document", response_model=GenerateDocsResponse)
async def generate_documentation(request: GenerateDocsRequest):
    """
    Generate documentation for code.
    
    - **code**: Code to document
    - **language**: Programming language
    - **doc_style**: Documentation style (google, numpy, sphinx)
    """
    # Check cache
    cached_response = ai_cache.get(request.code, request.language, f"document_{request.doc_style}")
    if cached_response:
        cached_response['cached'] = True
        return GenerateDocsResponse(**cached_response)
    
    try:
        # TODO: Replace with actual AI service call
        response_data = {
            "documentation": "Generated documentation in specified format...",
            "format": request.doc_style,
            "cached": False
        }
        
        # Cache the response
        ai_cache.set(request.code, request.language, f"document_{request.doc_style}", response_data)
        
        return GenerateDocsResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate documentation: {str(e)}"
        )


@router.get("/cache/stats")
async def get_cache_stats():
    """Get cache statistics."""
    return ai_cache.get_stats()


@router.post("/cache/clear-expired")
async def clear_expired_cache():
    """Clear expired cache entries."""
    deleted = ai_cache.clear_expired()
    return {"message": f"Cleared {deleted} expired cache entries"}
```

**Action Items:**
- [ ] Create all endpoints with mock responses
- [ ] Add proper error handling
- [ ] Test each endpoint with curl or Postman
- [ ] Update with real AI service when available

---

## 📝 Task 4: Update API Router

**File:** `backend/app/api/v1/__init__.py`

Add the AI router:

```python
from fastapi import APIRouter
from .endpoints import projects, analysis, ai

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(analysis.router, prefix="/projects", tags=["analysis"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])  # Add this line
```

**Action Items:**
- [ ] Add AI router to main API router
- [ ] Verify routes are registered
- [ ] Check API docs at http://localhost:8000/api/docs

---

## 🧪 Testing Checklist

### Test Schemas
```bash
cd backend
python -c "from app.schemas.ai import *; print('Schemas OK')"
```

### Test Cache
```bash
python -c "from app.utils.cache import ai_cache; print(ai_cache.get_stats())"
```

### Test Endpoints
```bash
# Explain code
curl -X POST "http://localhost:8000/api/v1/ai/explain" \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): print(\"hi\")", "language": "python"}'

# Get cache stats
curl "http://localhost:8000/api/v1/ai/cache/stats"
```

---

## ✅ Definition of Done

- [ ] All schemas created and validated
- [ ] Caching system implemented and tested
- [ ] All API endpoints created with mock responses
- [ ] API router updated
- [ ] Endpoints tested with curl/Postman
- [ ] API documentation updated
- [ ] Code committed to feature branch
- [ ] Ready for integration with Developer A's AI service

---

## 🤝 Integration with Developer A

Once Developer A completes the AI service:

1. Import the AI service:
   ```python
   from app.services.ai_service import ai_service
   ```

2. Replace mock responses with real AI calls:
   ```python
   explanation = ai_service.explain_code(request.code, request.language)
   ```

3. Test end-to-end functionality

4. Update cache keys if needed

---

## 📞 Need Help?

- Check with Developer A on AI service interface
- Coordinate in team chat
- Review STAGE_4_WORK_ASSIGNMENTS.md for overall context

**Good luck! 🚀**