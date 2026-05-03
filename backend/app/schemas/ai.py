"""
AI-related Pydantic schemas for code explanation, summarization, and documentation
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class ExplainCodeRequest(BaseModel):
    """Schema for code explanation request"""
    code: str = Field(..., description="Code snippet to explain")
    language: str = Field(..., description="Programming language of the code")
    context: Optional[str] = Field(None, description="Additional context about the code")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
                    "language": "python",
                    "context": "Recursive implementation"
                }
            ]
        }
    }


class ExplainCodeResponse(BaseModel):
    """Schema for code explanation response"""
    explanation: str = Field(..., description="Detailed explanation of the code")
    key_concepts: List[str] = Field(default_factory=list, description="Key programming concepts used")
    complexity_note: Optional[str] = Field(None, description="Note about code complexity")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    cached: bool = Field(default=False, description="Whether response was retrieved from cache")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "explanation": "This is a recursive factorial function...",
                    "key_concepts": ["recursion", "base case", "mathematical function"],
                    "complexity_note": "Time complexity: O(n), Space complexity: O(n) due to call stack",
                    "suggestions": ["Consider iterative approach for better space complexity"],
                    "cached": False
                }
            ]
        }
    }


class ExplainFileRequest(BaseModel):
    """Schema for file explanation request"""
    project_id: str = Field(..., description="Project ID containing the file")
    file_path: str = Field(..., description="Path to the file within the project")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "proj_abc123",
                    "file_path": "src/utils/helpers.py"
                }
            ]
        }
    }


class SummarizeRequest(BaseModel):
    """Schema for code summarization request"""
    code: str = Field(..., description="Code to summarize")
    language: str = Field(..., description="Programming language of the code")
    summary_type: str = Field(default="brief", description="Type of summary (brief, detailed, technical)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "class UserManager:\n    def create_user(self, name, email):\n        pass",
                    "language": "python",
                    "summary_type": "brief"
                }
            ]
        }
    }


class SummarizeResponse(BaseModel):
    """Schema for code summarization response"""
    summary: str = Field(..., description="Summary of the code")
    main_purpose: str = Field(..., description="Main purpose of the code")
    key_functions: List[str] = Field(default_factory=list, description="Key functions or methods")
    dependencies: List[str] = Field(default_factory=list, description="External dependencies")
    cached: bool = Field(default=False, description="Whether response was retrieved from cache")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "summary": "User management class with CRUD operations",
                    "main_purpose": "Manage user accounts and authentication",
                    "key_functions": ["create_user", "update_user", "delete_user"],
                    "dependencies": ["database", "auth_service"],
                    "cached": False
                }
            ]
        }
    }


class GenerateDocsRequest(BaseModel):
    """Schema for documentation generation request"""
    code: str = Field(..., description="Code to document")
    language: str = Field(..., description="Programming language of the code")
    doc_style: str = Field(default="google", description="Documentation style (google, numpy, sphinx)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "def calculate_total(items, tax_rate=0.1):\n    return sum(items) * (1 + tax_rate)",
                    "language": "python",
                    "doc_style": "google"
                }
            ]
        }
    }


class GenerateDocsResponse(BaseModel):
    """Schema for documentation generation response"""
    documentation: str = Field(..., description="Generated documentation")
    format: str = Field(..., description="Documentation format used")
    cached: bool = Field(default=False, description="Whether response was retrieved from cache")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "documentation": "\"\"\"Calculate total with tax.\n\nArgs:\n    items: List of item prices\n    tax_rate: Tax rate (default 0.1)\n\nReturns:\n    Total amount with tax\n\"\"\"",
                    "format": "google",
                    "cached": False
                }
            ]
        }
    }

# Made with Bob