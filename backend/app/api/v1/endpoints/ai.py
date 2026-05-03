"""
AI-powered code analysis endpoints
"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.ai import (
    ExplainCodeRequest, ExplainCodeResponse, ExplainFileRequest,
    SummarizeRequest, SummarizeResponse, GenerateDocsRequest, GenerateDocsResponse
)
from app.utils.cache import ai_cache
from app.utils.storage import storage

# from app.services.ai_service import ai_service

router = APIRouter()


@router.post("/explain", response_model=ExplainCodeResponse)
async def explain_code(request: ExplainCodeRequest):
    """
    Explain a code snippet with AI-powered analysis
    
    Args:
        request: Code explanation request with code, language, and optional context
    
    Returns:
        Detailed explanation with key concepts and suggestions
    """
    try:
        # Check cache first
        cached_response = ai_cache.get(request.code, request.language, "explain")
        if cached_response:
            cached_response['cached'] = True
            return ExplainCodeResponse(**cached_response)
        
        # TODO: Replace with actual AI service call
        # response_data = ai_service.explain_code(request.code, request.language, request.context)
        
        # Mock response
        response_data = {
            "explanation": f"This {request.language} code demonstrates a common programming pattern. "
                          f"The code structure follows best practices for {request.language} development.",
            "key_concepts": [
                "control flow",
                "data structures",
                f"{request.language} syntax"
            ],
            "complexity_note": "The code has moderate complexity with O(n) time complexity",
            "suggestions": [
                "Consider adding error handling",
                "Add type hints for better code clarity",
                "Include docstrings for documentation"
            ],
            "cached": False
        }
        
        # Save to cache
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
    Explain a file from a project with AI-powered analysis
    
    Args:
        request: File explanation request with project_id and file_path
    
    Returns:
        Detailed explanation of the file's purpose and structure
    """
    try:
        # Validate project exists
        project = storage.get_project(request.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {request.project_id} not found"
            )
        
        # For now, use a mock file content
        # In real implementation, would read file from project directory
        mock_code = f"# File: {request.file_path}\n# Project: {project['name']}"
        language = request.file_path.split('.')[-1] if '.' in request.file_path else "unknown"
        
        # Check cache
        cached_response = ai_cache.get(mock_code, language, "explain")
        if cached_response:
            cached_response['cached'] = True
            return ExplainCodeResponse(**cached_response)
        
        # TODO: Replace with actual AI service call
        # file_content = read_project_file(request.project_id, request.file_path)
        # response_data = ai_service.explain_code(file_content, language)
        
        # Mock response
        response_data = {
            "explanation": f"This file ({request.file_path}) is part of the {project['name']} project. "
                          f"It contains important functionality for the application.",
            "key_concepts": [
                "modular design",
                "separation of concerns",
                f"{language} best practices"
            ],
            "complexity_note": "The file has well-structured code with clear responsibilities",
            "suggestions": [
                "Consider splitting into smaller modules if file grows",
                "Add comprehensive unit tests",
                "Document public APIs"
            ],
            "cached": False
        }
        
        # Save to cache
        ai_cache.set(mock_code, language, "explain", response_data)
        
        return ExplainCodeResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain file: {str(e)}"
        )


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_code(request: SummarizeRequest):
    """
    Generate a summary of code with AI analysis
    
    Args:
        request: Summarization request with code, language, and summary type
    
    Returns:
        Code summary with main purpose, key functions, and dependencies
    """
    try:
        # Check cache first
        cache_key = f"summarize_{request.summary_type}"
        cached_response = ai_cache.get(request.code, request.language, cache_key)
        if cached_response:
            cached_response['cached'] = True
            return SummarizeResponse(**cached_response)
        
        # TODO: Replace with actual AI service call
        # response_data = ai_service.summarize_code(request.code, request.language, request.summary_type)
        
        # Mock response
        summary_detail = "detailed" if request.summary_type == "detailed" else "brief"
        response_data = {
            "summary": f"This {request.language} code provides {summary_detail} functionality "
                      f"for handling core application logic.",
            "main_purpose": f"Implements key features using {request.language} patterns",
            "key_functions": [
                "main_function",
                "helper_method",
                "utility_function"
            ],
            "dependencies": [
                "standard_library",
                "external_package"
            ],
            "cached": False
        }
        
        # Save to cache
        ai_cache.set(request.code, request.language, cache_key, response_data)
        
        return SummarizeResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarize code: {str(e)}"
        )


@router.post("/document", response_model=GenerateDocsResponse)
async def generate_documentation(request: GenerateDocsRequest):
    """
    Generate documentation for code using AI
    
    Args:
        request: Documentation request with code, language, and doc style
    
    Returns:
        Generated documentation in specified format
    """
    try:
        # Check cache first
        cache_key = f"document_{request.doc_style}"
        cached_response = ai_cache.get(request.code, request.language, cache_key)
        if cached_response:
            cached_response['cached'] = True
            return GenerateDocsResponse(**cached_response)
        
        # TODO: Replace with actual AI service call
        # response_data = ai_service.generate_docs(request.code, request.language, request.doc_style)
        
        # Mock response based on doc style
        if request.doc_style == "google":
            doc_template = '''"""
Summary of the function or class.

Args:
    param1: Description of first parameter
    param2: Description of second parameter

Returns:
    Description of return value

Raises:
    ExceptionType: Description of when this exception is raised
"""'''
        elif request.doc_style == "numpy":
            doc_template = '''"""
Summary of the function or class.

Parameters
----------
param1 : type
    Description of first parameter
param2 : type
    Description of second parameter

Returns
-------
type
    Description of return value
"""'''
        else:  # sphinx
            doc_template = '''"""
Summary of the function or class.

:param param1: Description of first parameter
:param param2: Description of second parameter
:return: Description of return value
:raises ExceptionType: Description of when this exception is raised
"""'''
        
        response_data = {
            "documentation": doc_template,
            "format": request.doc_style,
            "cached": False
        }
        
        # Save to cache
        ai_cache.set(request.code, request.language, cache_key, response_data)
        
        return GenerateDocsResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate documentation: {str(e)}"
        )


@router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache statistics
    
    Returns:
        Dictionary with cache statistics including total entries and size
    """
    try:
        stats = ai_cache.get_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cache stats: {str(e)}"
        )


@router.post("/cache/clear-expired")
async def clear_expired_cache():
    """
    Clear expired cache entries
    
    Returns:
        Dictionary with number of entries deleted
    """
    try:
        deleted_count = ai_cache.clear_expired()
        return {
            "deleted_count": deleted_count,
            "message": f"Cleared {deleted_count} expired cache entries"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear expired cache: {str(e)}"
        )

# Made with Bob