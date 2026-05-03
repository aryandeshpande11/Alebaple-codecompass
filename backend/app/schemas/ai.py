"""
AI-related Pydantic schemas for request/response validation
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    """Schema for code explanation request"""
    code: str = Field(..., description="Code snippet to explain", min_length=1)
    language: str = Field(
        ..., 
        description="Programming language (python, java, javascript, typescript)",
        pattern="^(python|java|javascript|typescript)$"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "def hello():\n    print('Hello, World!')",
                    "language": "python"
                }
            ]
        }
    }


class ExplainResponse(BaseModel):
    """Schema for code explanation response"""
    explanation: str = Field(..., description="Detailed code explanation")
    language: str = Field(..., description="Programming language")
    code_length: int = Field(..., description="Length of code in characters")
    timestamp: str = Field(..., description="Response timestamp (ISO 8601)")
    duration_seconds: float = Field(..., description="Processing time in seconds")
    model: str = Field(..., description="AI model used")
    mock: bool = Field(..., description="Whether this is a mock response")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "explanation": "This Python function prints 'Hello, World!' to the console...",
                    "language": "python",
                    "code_length": 45,
                    "timestamp": "2026-05-02T18:00:00Z",
                    "duration_seconds": 0.5,
                    "model": "ibm/granite-13b-chat-v2",
                    "mock": True
                }
            ]
        }
    }


class ExplainFileRequest(BaseModel):
    """Schema for file explanation request"""
    file_content: str = Field(..., description="Complete file content", min_length=1)
    language: str = Field(
        ..., 
        description="Programming language",
        pattern="^(python|java|javascript|typescript)$"
    )
    file_path: Optional[str] = Field(None, description="Optional file path for context")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "file_content": "# Python module\ndef main():\n    pass",
                    "language": "python",
                    "file_path": "src/main.py"
                }
            ]
        }
    }


class SummaryRequest(BaseModel):
    """Schema for code summary request"""
    content: str = Field(..., description="Code content to summarize", min_length=1)
    language: str = Field(
        ..., 
        description="Programming language",
        pattern="^(python|java|javascript|typescript)$"
    )
    context: Optional[str] = Field(None, description="Additional context (file path, module name, etc.)")
    summary_type: str = Field(
        default="file",
        description="Type of summary (file, class, function)",
        pattern="^(file|class|function)$"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": "class MyClass:\n    def __init__(self):\n        pass",
                    "language": "python",
                    "context": "MyClass",
                    "summary_type": "class"
                }
            ]
        }
    }


class SummaryResponse(BaseModel):
    """Schema for code summary response"""
    summary: str = Field(..., description="Code summary")
    language: str = Field(..., description="Programming language")
    content_size: int = Field(..., description="Size of content in characters")
    context: Optional[str] = Field(None, description="Context provided")
    summary_type: str = Field(..., description="Type of summary")
    timestamp: str = Field(..., description="Response timestamp (ISO 8601)")
    duration_seconds: float = Field(..., description="Processing time in seconds")
    model: str = Field(..., description="AI model used")
    mock: bool = Field(..., description="Whether this is a mock response")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "summary": "This class provides basic functionality...",
                    "language": "python",
                    "content_size": 150,
                    "context": "MyClass",
                    "summary_type": "class",
                    "timestamp": "2026-05-02T18:00:00Z",
                    "duration_seconds": 0.3,
                    "model": "ibm/granite-13b-chat-v2",
                    "mock": True
                }
            ]
        }
    }


class DocumentationRequest(BaseModel):
    """Schema for documentation generation request"""
    code: str = Field(..., description="Code to document", min_length=1)
    language: str = Field(
        ..., 
        description="Programming language",
        pattern="^(python|java|javascript|typescript)$"
    )
    doc_style: Optional[str] = Field(
        None, 
        description="Documentation style (google, numpy, sphinx, javadoc, jsdoc)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "def calculate(x, y):\n    return x + y",
                    "language": "python",
                    "doc_style": "google"
                }
            ]
        }
    }


class DocumentationResponse(BaseModel):
    """Schema for documentation generation response"""
    documentation: str = Field(..., description="Generated documentation")
    language: str = Field(..., description="Programming language")
    code_length: int = Field(..., description="Length of code in characters")
    doc_style: Optional[str] = Field(None, description="Documentation style used")
    timestamp: str = Field(..., description="Response timestamp (ISO 8601)")
    duration_seconds: float = Field(..., description="Processing time in seconds")
    model: str = Field(..., description="AI model used")
    mock: bool = Field(..., description="Whether this is a mock response")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "documentation": "**Function: calculate**\n\nCalculates the sum...",
                    "language": "python",
                    "code_length": 50,
                    "doc_style": "google",
                    "timestamp": "2026-05-02T18:00:00Z",
                    "duration_seconds": 0.4,
                    "model": "ibm/granite-13b-chat-v2",
                    "mock": True
                }
            ]
        }
    }


class AIHealthResponse(BaseModel):
    """Schema for AI service health check response"""
    status: str = Field(..., description="Service status (healthy, degraded, unhealthy)")
    mock_mode: bool = Field(..., description="Whether service is in mock mode")
    configured: bool = Field(..., description="Whether watsonx.ai is properly configured")
    model: str = Field(..., description="AI model being used")
    timestamp: str = Field(..., description="Response timestamp (ISO 8601)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "mock_mode": True,
                    "configured": False,
                    "model": "ibm/granite-13b-chat-v2",
                    "timestamp": "2026-05-02T18:00:00Z"
                }
            ]
        }
    }


class AIErrorResponse(BaseModel):
    """Schema for AI service error response"""
    error: str = Field(..., description="Error message")
    language: Optional[str] = Field(None, description="Programming language if applicable")
    timestamp: str = Field(..., description="Error timestamp (ISO 8601)")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Failed to process request",
                    "language": "python",
                    "timestamp": "2026-05-02T18:00:00Z",
                    "details": {"reason": "Invalid input"}
                }
            ]
        }
    }


class BatchExplainRequest(BaseModel):
    """Schema for batch code explanation request"""
    items: List[Dict[str, str]] = Field(
        ..., 
        description="List of code items to explain",
        min_length=1,
        max_length=10
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "items": [
                        {"code": "def hello():\n    pass", "language": "python"},
                        {"code": "function hello() {}", "language": "javascript"}
                    ]
                }
            ]
        }
    }


class BatchExplainResponse(BaseModel):
    """Schema for batch code explanation response"""
    results: List[ExplainResponse] = Field(..., description="List of explanation results")
    total_items: int = Field(..., description="Total number of items processed")
    successful: int = Field(..., description="Number of successful explanations")
    failed: int = Field(..., description="Number of failed explanations")
    total_duration_seconds: float = Field(..., description="Total processing time")
    timestamp: str = Field(..., description="Response timestamp (ISO 8601)")


# Made with Bob