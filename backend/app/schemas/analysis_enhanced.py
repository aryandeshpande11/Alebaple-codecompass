"""
Enhanced Analysis Schemas with AI Integration
Extends base analysis schemas with AI-generated insights
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from app.schemas.analysis import FunctionInfo, ClassInfo, FileAnalysis, CodeMetrics


class AIInsight(BaseModel):
    """Schema for AI-generated insight"""
    type: str = Field(..., description="Type of insight (explanation, summary, documentation)")
    content: str = Field(..., description="AI-generated content")
    language: str = Field(..., description="Programming language")
    timestamp: str = Field(..., description="When the insight was generated")
    model: str = Field(..., description="AI model used")
    from_cache: bool = Field(default=False, description="Whether loaded from cache")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "explanation",
                    "content": "This function implements...",
                    "language": "python",
                    "timestamp": "2026-05-02T18:00:00Z",
                    "model": "ibm/granite-13b-chat-v2",
                    "from_cache": False
                }
            ]
        }
    }


class FunctionWithAI(FunctionInfo):
    """Function information with AI explanation"""
    ai_explanation: Optional[AIInsight] = Field(None, description="AI-generated explanation")
    importance_score: Optional[int] = Field(None, description="Calculated importance score")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "calculate_total",
                    "line_number": 10,
                    "args": ["items", "tax_rate"],
                    "docstring": "Calculate total with tax",
                    "complexity": 5,
                    "ai_explanation": {
                        "type": "explanation",
                        "content": "This function calculates...",
                        "language": "python",
                        "timestamp": "2026-05-02T18:00:00Z",
                        "model": "ibm/granite-13b-chat-v2",
                        "from_cache": False
                    },
                    "importance_score": 7
                }
            ]
        }
    }


class ClassWithAI(ClassInfo):
    """Class information with AI explanation"""
    ai_explanation: Optional[AIInsight] = Field(None, description="AI-generated explanation")
    importance_score: Optional[int] = Field(None, description="Calculated importance score")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "DataProcessor",
                    "line_number": 5,
                    "methods": ["process", "validate", "save"],
                    "docstring": "Processes data from various sources",
                    "ai_explanation": {
                        "type": "explanation",
                        "content": "This class provides...",
                        "language": "python",
                        "timestamp": "2026-05-02T18:00:00Z",
                        "model": "ibm/granite-13b-chat-v2",
                        "from_cache": False
                    },
                    "importance_score": 8
                }
            ]
        }
    }


class FileAnalysisWithAI(FileAnalysis):
    """File analysis with AI insights"""
    ai_summary: Optional[AIInsight] = Field(None, description="AI-generated file summary")
    ai_documentation: Optional[AIInsight] = Field(None, description="AI-generated documentation")
    important_functions: List[FunctionWithAI] = Field(
        default_factory=list,
        description="Important functions with AI explanations"
    )
    important_classes: List[ClassWithAI] = Field(
        default_factory=list,
        description="Important classes with AI explanations"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "path": "src/main.py",
                    "lines_of_code": 150,
                    "functions": [],
                    "classes": [],
                    "imports": ["os", "sys"],
                    "complexity": 6.5,
                    "ai_summary": {
                        "type": "summary",
                        "content": "This file serves as...",
                        "language": "python",
                        "timestamp": "2026-05-02T18:00:00Z",
                        "model": "ibm/granite-13b-chat-v2",
                        "from_cache": False
                    },
                    "important_functions": [],
                    "important_classes": []
                }
            ]
        }
    }


class ProjectAnalysisWithAI(BaseModel):
    """Complete project analysis with AI insights"""
    project_id: str = Field(..., description="Project ID")
    status: str = Field(..., description="Analysis status")
    
    # Base analysis data
    metrics: Optional[CodeMetrics] = Field(None, description="Code metrics summary")
    files: List[FileAnalysisWithAI] = Field(
        default_factory=list,
        description="Per-file analysis with AI insights"
    )
    
    # AI-specific data
    ai_enabled: bool = Field(default=False, description="Whether AI analysis was performed")
    ai_summary: Optional[str] = Field(None, description="Overall project AI summary")
    key_insights: List[str] = Field(
        default_factory=list,
        description="Key insights from AI analysis"
    )
    
    # Prioritization data
    priority_files: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Files prioritized for review"
    )
    
    # Timestamps
    started_at: Optional[datetime] = Field(None, description="Analysis start time")
    completed_at: Optional[datetime] = Field(None, description="Analysis completion time")
    ai_processing_time: Optional[float] = Field(None, description="Time spent on AI processing")
    
    # Error handling
    error: Optional[str] = Field(None, description="Error message if failed")
    ai_errors: List[str] = Field(
        default_factory=list,
        description="AI-specific errors encountered"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "proj_abc123",
                    "status": "completed",
                    "metrics": {
                        "total_files": 15,
                        "total_lines": 2500,
                        "total_functions": 45,
                        "total_classes": 12,
                        "average_complexity": 6.5,
                        "comment_ratio": 0.15
                    },
                    "files": [],
                    "ai_enabled": True,
                    "ai_summary": "This project implements a web application...",
                    "key_insights": [
                        "High complexity in authentication module",
                        "Well-documented API endpoints",
                        "Consider refactoring database layer"
                    ],
                    "priority_files": [],
                    "started_at": "2026-05-02T15:30:00Z",
                    "completed_at": "2026-05-02T15:35:00Z",
                    "ai_processing_time": 45.5,
                    "error": None,
                    "ai_errors": []
                }
            ]
        }
    }


class EnhancedAnalysisRequest(BaseModel):
    """Request for enhanced analysis with AI"""
    project_id: str = Field(..., description="Project ID to analyze")
    enable_ai: bool = Field(default=True, description="Enable AI analysis")
    max_files_for_ai: int = Field(
        default=10,
        description="Maximum number of files to analyze with AI",
        ge=1,
        le=50
    )
    include_function_explanations: bool = Field(
        default=True,
        description="Include AI explanations for important functions"
    )
    include_class_explanations: bool = Field(
        default=True,
        description="Include AI explanations for important classes"
    )
    include_file_summaries: bool = Field(
        default=True,
        description="Include AI summaries for files"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "proj_abc123",
                    "enable_ai": True,
                    "max_files_for_ai": 10,
                    "include_function_explanations": True,
                    "include_class_explanations": True,
                    "include_file_summaries": True
                }
            ]
        }
    }


class EnhancedAnalysisResponse(BaseModel):
    """Response for enhanced analysis"""
    project_id: str = Field(..., description="Project ID")
    status: str = Field(..., description="Analysis status")
    message: str = Field(..., description="Status message")
    analysis_id: Optional[str] = Field(None, description="Analysis ID for tracking")
    estimated_time_seconds: Optional[int] = Field(
        None,
        description="Estimated time for completion"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "project_id": "proj_abc123",
                    "status": "processing",
                    "message": "Enhanced analysis started with AI integration",
                    "analysis_id": "analysis_xyz789",
                    "estimated_time_seconds": 120
                }
            ]
        }
    }


class AIProcessingStats(BaseModel):
    """Statistics for AI processing"""
    total_requests: int = Field(..., description="Total AI requests made")
    successful_requests: int = Field(..., description="Successful AI requests")
    failed_requests: int = Field(..., description="Failed AI requests")
    cached_responses: int = Field(..., description="Responses served from cache")
    total_processing_time: float = Field(..., description="Total AI processing time in seconds")
    average_response_time: float = Field(..., description="Average response time in seconds")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_requests": 25,
                    "successful_requests": 23,
                    "failed_requests": 2,
                    "cached_responses": 10,
                    "total_processing_time": 45.5,
                    "average_response_time": 1.82
                }
            ]
        }
    }


# Made with Bob