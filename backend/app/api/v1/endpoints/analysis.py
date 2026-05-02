"""
Code analysis API endpoints
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
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
from app.services.code_analyzer import CodeAnalyzer

router = APIRouter()

# Initialize code analyzer
analyzer = CodeAnalyzer()


def perform_analysis(project_id: str, repo_url: str):
    """Background task to perform code analysis."""
    try:
        # Run the analysis
        analysis_result = analyzer.analyze_repository(repo_url, project_id)
        
        # Store analysis results
        storage.create_analysis(project_id, analysis_result)
        
        # Update project status
        if analysis_result["status"] == "completed":
            storage.update_project(project_id, {"status": "completed"})
        else:
            storage.update_project(project_id, {"status": "failed"})
    
    except Exception as e:
        # Store error in analysis
        error_result = {
            "project_id": project_id,
            "status": "failed",
            "error": str(e),
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }
        storage.create_analysis(project_id, error_result)
        storage.update_project(project_id, {"status": "failed"})


@router.post("/{project_id}/analyze", response_model=dict)
async def analyze_project(project_id: str, background_tasks: BackgroundTasks):
    """
    Trigger code analysis for a project
    
    - **project_id**: Unique project identifier
    
    This endpoint will analyze the project's code and generate comprehensive metrics.
    Analysis runs in the background and results can be retrieved via GET endpoint.
    """
    # Check if project exists
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    # Check if project has a repository URL
    repo_url = project.get("repository_url")
    if not repo_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project does not have a repository URL"
        )
    
    # Update project status to analyzing
    storage.update_project(project_id, {"status": "analyzing"})
    
    # Start analysis in background
    background_tasks.add_task(perform_analysis, project_id, repo_url)
    
    return {
        "message": "Analysis started",
        "project_id": project_id,
        "status": "analyzing"
    }


@router.get("/{project_id}/analysis")
async def get_analysis(project_id: str):
    """
    Get analysis results for a project
    
    - **project_id**: Unique project identifier
    
    Returns the comprehensive analysis results if available
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
    
    return analysis


@router.get("/{project_id}/files/{file_path:path}")
async def get_file_analysis(project_id: str, file_path: str):
    """
    Get detailed analysis for a specific file
    
    - **project_id**: Unique project identifier
    - **file_path**: Path to the file (relative to project root)
    
    Returns detailed analysis for the specified file
    """
    # Check if project exists
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    try:
        file_analysis = analyzer.get_file_analysis(project_id, file_path)
        
        if "error" in file_analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=file_analysis["error"]
            )
        
        return file_analysis
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file analysis: {str(e)}"
        )

# Made with Bob
