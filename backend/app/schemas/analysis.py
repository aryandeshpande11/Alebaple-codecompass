"""
Analysis-related Pydantic schemas
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class FunctionInfo(BaseModel):
    """Schema for function information"""
    name: str = Field(..., description="Function name")
    line_number: int = Field(..., description="Starting line number")
    args: List[str] = Field(default_factory=list, description="Function arguments")
    docstring: Optional[str] = Field(None, description="Function docstring")
    complexity: Optional[int] = Field(None, description="Cyclomatic complexity")


class ClassInfo(BaseModel):
    """Schema for class information"""
    name: str = Field(..., description="Class name")
    line_number: int = Field(..., description="Starting line number")
    methods: List[str] = Field(default_factory=list, description="Class methods")
    docstring: Optional[str] = Field(None, description="Class docstring")


class FileAnalysis(BaseModel):
    """Schema for individual file analysis"""
    path: str = Field(..., description="File path relative to project root")
    lines_of_code: int = Field(..., description="Total lines of code")
    functions: List[FunctionInfo] = Field(default_factory=list, description="Functions in file")
    classes: List[ClassInfo] = Field(default_factory=list, description="Classes in file")
    imports: List[str] = Field(default_factory=list, description="Import statements")
    complexity: Optional[float] = Field(None, description="Average complexity")


class CodeMetrics(BaseModel):
    """Schema for code metrics summary"""
    total_files: int = Field(..., description="Total number of Python files")
    total_lines: int = Field(..., description="Total lines of code")
    total_functions: int = Field(..., description="Total number of functions")
    total_classes: int = Field(..., description="Total number of classes")
    average_complexity: Optional[float] = Field(None, description="Average cyclomatic complexity")
    comment_ratio: Optional[float] = Field(None, description="Ratio of comments to code")


class AnalysisRequest(BaseModel):
    """Schema for analysis request"""
    project_id: str = Field(..., description="Project ID to analyze")
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Analysis options (e.g., include_tests, max_depth)"
    )


class AnalysisResponse(BaseModel):
    """Schema for analysis response"""
    project_id: str = Field(..., description="Project ID")
    status: str = Field(..., description="Analysis status (pending, running, completed, failed)")
    metrics: Optional[CodeMetrics] = Field(None, description="Code metrics summary")
    files: List[FileAnalysis] = Field(default_factory=list, description="Per-file analysis")
    started_at: Optional[datetime] = Field(None, description="Analysis start time")
    completed_at: Optional[datetime] = Field(None, description="Analysis completion time")
    error: Optional[str] = Field(None, description="Error message if failed")
    
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
                    "started_at": "2026-05-02T15:30:00Z",
                    "completed_at": "2026-05-02T15:31:30Z",
                    "error": None
                }
            ]
        }
    }

# Made with Bob
