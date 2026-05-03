"""
AI endpoints for code explanation, summarization, and documentation
"""

from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.ai import (
    ExplainRequest,
    ExplainResponse,
    ExplainFileRequest,
    SummaryRequest,
    SummaryResponse,
    DocumentationRequest,
    DocumentationResponse,
    AIHealthResponse,
    AIErrorResponse,
    BatchExplainRequest,
    BatchExplainResponse,
)
from app.services.ai_service import get_ai_service, reload_ai_service
from app.utils.cache import get_cache

router = APIRouter()


@router.post(
    "/explain",
    response_model=ExplainResponse,
    status_code=status.HTTP_200_OK,
    summary="Explain code snippet",
    description="Get a detailed explanation of a code snippet using IBM watsonx.ai",
    responses={
        200: {"description": "Code explanation generated successfully"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"},
    }
)
async def explain_code(request: ExplainRequest) -> ExplainResponse:
    """
    Explain a code snippet
    
    - **code**: The code snippet to explain
    - **language**: Programming language (python, java, javascript, typescript)
    
    Returns a detailed explanation including:
    - Overview of what the code does
    - Key components and their purposes
    - Logic flow and algorithms
    - Dependencies and imports
    - Complexity assessment
    - Best practices and potential improvements
    """
    try:
        # Check cache first
        cache = get_cache()
        cached_response = cache.get(request.code, request.language, "explain")
        
        if cached_response:
            return ExplainResponse(**cached_response)
        
        # Get AI service and generate explanation
        ai_service = get_ai_service()
        result = ai_service.explain_code(request.code, request.language)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Cache the response
        cache.set(request.code, request.language, "explain", result)
        
        return ExplainResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain code: {str(e)}"
        )


@router.post(
    "/explain-file",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Explain entire file",
    description="Get a summary explanation of an entire code file",
    responses={
        200: {"description": "File explanation generated successfully"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"},
    }
)
async def explain_file(request: ExplainFileRequest) -> SummaryResponse:
    """
    Explain an entire code file
    
    - **file_content**: Complete file content
    - **language**: Programming language
    - **file_path**: Optional file path for context
    
    Returns a comprehensive file summary including:
    - Purpose of the file
    - Key exports (classes, functions, components)
    - Dependencies
    - Complexity level
    - Role in the project
    """
    try:
        # Check cache first
        cache = get_cache()
        cached_response = cache.get(request.file_content, request.language, "summarize_file")
        
        if cached_response:
            return SummaryResponse(
                summary=cached_response.get("summary", ""),
                language=cached_response.get("language", request.language),
                content_size=cached_response.get("file_size", len(request.file_content)),
                context=request.file_path,
                summary_type="file",
                timestamp=cached_response.get("timestamp", ""),
                duration_seconds=cached_response.get("duration_seconds", 0),
                model=cached_response.get("model", ""),
                mock=cached_response.get("mock", True)
            )
        
        # Get AI service and generate summary
        ai_service = get_ai_service()
        result = ai_service.summarize_file(
            request.file_content, 
            request.language, 
            request.file_path or ""
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Cache the response
        cache.set(request.file_content, request.language, "summarize_file", result)
        
        return SummaryResponse(
            summary=result.get("summary", ""),
            language=result.get("language", request.language),
            content_size=result.get("file_size", len(request.file_content)),
            context=request.file_path,
            summary_type="file",
            timestamp=result.get("timestamp", ""),
            duration_seconds=result.get("duration_seconds", 0),
            model=result.get("model", ""),
            mock=result.get("mock", True)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to explain file: {str(e)}"
        )


@router.post(
    "/summarize",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize code",
    description="Get a concise summary of code (file, class, or function)",
    responses={
        200: {"description": "Summary generated successfully"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"},
    }
)
async def summarize_code(request: SummaryRequest) -> SummaryResponse:
    """
    Summarize code content
    
    - **content**: Code content to summarize
    - **language**: Programming language
    - **context**: Additional context (file path, class name, function name)
    - **summary_type**: Type of summary (file, class, function)
    
    Returns a concise summary appropriate for the summary type
    """
    try:
        # Check cache first
        cache = get_cache()
        cache_key_suffix = f"{request.summary_type}_{request.context or 'default'}"
        cached_response = cache.get(
            request.content + cache_key_suffix, 
            request.language, 
            f"summarize_{request.summary_type}"
        )
        
        if cached_response:
            return SummaryResponse(
                summary=cached_response.get("summary", ""),
                language=cached_response.get("language", request.language),
                content_size=len(request.content),
                context=request.context,
                summary_type=request.summary_type,
                timestamp=cached_response.get("timestamp", ""),
                duration_seconds=cached_response.get("duration_seconds", 0),
                model=cached_response.get("model", ""),
                mock=cached_response.get("mock", True)
            )
        
        # Get AI service and generate summary
        ai_service = get_ai_service()
        
        # Use appropriate method based on summary type
        if request.summary_type == "file":
            result = ai_service.summarize_file(
                request.content, 
                request.language, 
                request.context or ""
            )
        else:
            # For class/function, use the file summary method with context
            result = ai_service.summarize_file(
                request.content, 
                request.language, 
                f"{request.summary_type}: {request.context or 'unknown'}"
            )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Cache the response
        cache.set(
            request.content + cache_key_suffix, 
            request.language, 
            f"summarize_{request.summary_type}",
            result
        )
        
        return SummaryResponse(
            summary=result.get("summary", ""),
            language=result.get("language", request.language),
            content_size=len(request.content),
            context=request.context,
            summary_type=request.summary_type,
            timestamp=result.get("timestamp", ""),
            duration_seconds=result.get("duration_seconds", 0),
            model=result.get("model", ""),
            mock=result.get("mock", True)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarize code: {str(e)}"
        )


@router.post(
    "/document",
    response_model=DocumentationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate documentation",
    description="Generate comprehensive documentation for code",
    responses={
        200: {"description": "Documentation generated successfully"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"},
    }
)
async def generate_documentation(request: DocumentationRequest) -> DocumentationResponse:
    """
    Generate documentation for code
    
    - **code**: Code to document
    - **language**: Programming language
    - **doc_style**: Documentation style (optional)
    
    Returns comprehensive documentation including:
    - Module/class/function description
    - Parameters with types and descriptions
    - Return values
    - Exceptions/errors
    - Usage examples
    - Implementation notes
    """
    try:
        # Check cache first
        cache = get_cache()
        cache_key_suffix = f"_{request.doc_style}" if request.doc_style else ""
        cached_response = cache.get(
            request.code + cache_key_suffix, 
            request.language, 
            "document"
        )
        
        if cached_response:
            return DocumentationResponse(**cached_response)
        
        # Get AI service and generate documentation
        ai_service = get_ai_service()
        result = ai_service.generate_documentation(request.code, request.language)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Add doc_style to result
        result["doc_style"] = request.doc_style
        
        # Cache the response
        cache.set(
            request.code + cache_key_suffix, 
            request.language, 
            "document",
            result
        )
        
        return DocumentationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate documentation: {str(e)}"
        )


@router.get(
    "/health",
    response_model=AIHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="AI service health check",
    description="Check the health status of the AI service",
)
async def ai_health_check() -> AIHealthResponse:
    """
    Check AI service health
    
    Returns:
    - Service status
    - Mock mode status
    - Configuration status
    - Model information
    """
    try:
        ai_service = get_ai_service()
        health_info = ai_service.health_check()
        return AIHealthResponse(**health_info)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )


@router.get(
    "/cache/stats",
    status_code=status.HTTP_200_OK,
    summary="Get cache statistics",
    description="Get statistics about the AI response cache",
)
async def get_cache_statistics():
    """
    Get cache statistics
    
    Returns:
    - Cache hits and misses
    - Hit rate percentage
    - Number of cached items
    - Total cache size
    - TTL configuration
    """
    try:
        cache = get_cache()
        return cache.get_stats()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cache stats: {str(e)}"
        )


@router.delete(
    "/cache/clear",
    status_code=status.HTTP_200_OK,
    summary="Clear cache",
    description="Clear all cached AI responses",
)
async def clear_ai_cache():
    """
    Clear all cached responses
    
    Returns the number of cache entries deleted
    """
    try:
        cache = get_cache()
        count = cache.clear()
        return {
            "message": "Cache cleared successfully",
            "deleted_count": count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )


@router.delete(
    "/cache/clear-expired",
    status_code=status.HTTP_200_OK,
    summary="Clear expired cache",
    description="Clear only expired cached AI responses",
)
async def clear_expired_cache():
    """
    Clear expired cache entries
    
    Returns the number of expired cache entries deleted
    """
    try:
        cache = get_cache()
        count = cache.clear_expired()
        return {
            "message": "Expired cache cleared successfully",
            "deleted_count": count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear expired cache: {str(e)}"
        )

@router.post(
    "/reload",
    status_code=status.HTTP_200_OK,
    summary="Reload AI service",
    description="Reload the AI service to pick up new configuration changes",
)
async def reload_ai():
    """
    Reload the AI service instance
    
    Useful after updating .env file with new credentials.
    Forces the AI service to reinitialize with current environment variables.
    """
    try:
        service = reload_ai_service()
        config = service.config
        
        return {
            "message": "AI service reloaded successfully",
            "mock_mode": config.use_mock_responses,
            "configured": config.is_configured(),
            "model": config.watsonx_model_id,
            "has_api_key": bool(config.watsonx_api_key),
            "has_project_id": bool(config.watsonx_project_id)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reload AI service: {str(e)}"
        )



# Made with Bob