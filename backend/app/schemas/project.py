"""
Project-related Pydantic schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub repository URL")
    description: Optional[str] = Field(None, max_length=1000, description="Project description")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "My Python Project",
                    "github_url": "https://github.com/user/repo",
                    "description": "A sample Python project for analysis"
                }
            ]
        }
    }


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class ProjectResponse(BaseModel):
    """Schema for project response"""
    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    github_url: Optional[str] = Field(None, description="GitHub repository URL")
    description: Optional[str] = Field(None, description="Project description")
    status: str = Field(..., description="Project status (pending, analyzing, completed, failed)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "proj_abc123",
                    "name": "My Python Project",
                    "github_url": "https://github.com/user/repo",
                    "description": "A sample Python project",
                    "status": "pending",
                    "created_at": "2026-05-02T15:30:00Z",
                    "updated_at": "2026-05-02T15:30:00Z"
                }
            ]
        }
    }


class ProjectList(BaseModel):
    """Schema for list of projects"""
    projects: list[ProjectResponse] = Field(..., description="List of projects")
    total: int = Field(..., description="Total number of projects")

# Made with Bob
