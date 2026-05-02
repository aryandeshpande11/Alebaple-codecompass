"""
Code analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from app.schemas.analysis import (
    AnalysisRequest,
    AnalysisResponse,
    CodeMetrics,
    FileAnalysis,
    FunctionInfo,
    ClassInfo
)
from app.utils.storage import storage

router = APIRouter()


@router.post("/{project_id}/analyze", response_model=AnalysisResponse)
async def analyze_project(project_id: str):
    """
    Trigger code analysis for a project
    
    - **project_id**: Unique project identifier
    
    This endpoint will analyze the project's code and generate metrics.
    For now, it returns mock data. Real analysis will be implemented in Stage 3.
    """
    # Check if project exists
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    # Update project status to analyzing
    storage.update_project(project_id, {"status": "analyzing"})
    
    try:
        # Create mock analysis data for now
        # Real analysis will be implemented in Stage 3
        analysis_data = {
            "project_id": project_id,
            "status": "completed",
            "metrics": {
                "total_files": 15,
                "total_lines": 2500,
                "total_functions": 45,
                "total_classes": 12,
                "average_complexity": 6.5,
                "comment_ratio": 0.15
            },
            "files": [
                {
                    "path": "src/main.py",
                    "lines_of_code": 150,
                    "functions": [
                        {
                            "name": "main",
                            "line_number": 10,
                            "args": [],
                            "docstring": "Main entry point",
                            "complexity": 5
                        }
                    ],
                    "classes": [],
                    "imports": ["fastapi", "uvicorn"],
                    "complexity": 5.0
                }
            ],
            "started_at": datetime.utcnow().isoformat(),
            "completed_at": datetime.utcnow().isoformat(),
            "error": None
        }
        
        # Store analysis results
        storage.create_analysis(project_id, analysis_data)
        
        # Update project status to completed
        storage.update_project(project_id, {"status": "completed"})
        
        return AnalysisResponse(**analysis_data)
    
    except Exception as e:
        # Update project status to failed
        storage.update_project(project_id, {"status": "failed"})
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/{project_id}/analysis", response_model=AnalysisResponse)
async def get_analysis(project_id: str):
    """
    Get analysis results for a project
    
    - **project_id**: Unique project identifier
    
    Returns the analysis results if available
    """
    # Check if project exists
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    # Get analysis results
    analysis = storage.get_analysis(project_id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for project '{project_id}'. Run analysis first."
        )
    
    return AnalysisResponse(**analysis)

# Made with Bob
