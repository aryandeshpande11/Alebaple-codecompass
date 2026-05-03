"""
Enhanced Analysis Endpoints with AI Integration
Provides code analysis with AI-generated explanations and insights
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, status
from typing import Dict, Any
import logging

from app.schemas.analysis_enhanced import (
    EnhancedAnalysisRequest,
    EnhancedAnalysisResponse,
    ProjectAnalysisWithAI,
    AIProcessingStats,
)
from app.services.code_analyzer import CodeAnalyzer
from app.services.analysis_ai_integration import get_integration_service
from app.utils.storage import load_project, save_analysis_result

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/{project_id}/analyze-with-ai",
    response_model=EnhancedAnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Analyze project with AI insights",
    description="Perform code analysis with AI-generated explanations and insights",
    responses={
        202: {"description": "Analysis started successfully"},
        404: {"description": "Project not found"},
        500: {"description": "Internal server error"},
    }
)
async def analyze_project_with_ai(
    project_id: str,
    request: EnhancedAnalysisRequest,
    background_tasks: BackgroundTasks
) -> EnhancedAnalysisResponse:
    """
    Analyze a project with AI integration
    
    This endpoint triggers a comprehensive analysis that includes:
    - Standard code analysis (structure, metrics, dependencies)
    - AI-generated explanations for important functions and classes
    - AI summaries for key files
    - Project-level insights and recommendations
    
    The analysis runs in the background and results are stored for later retrieval.
    
    Parameters:
    - **project_id**: ID of the project to analyze
    - **enable_ai**: Enable AI analysis (default: true)
    - **max_files_for_ai**: Maximum files to analyze with AI (default: 10)
    - **include_function_explanations**: Include AI explanations for functions
    - **include_class_explanations**: Include AI explanations for classes
    - **include_file_summaries**: Include AI summaries for files
    """
    try:
        # Verify project exists
        project = load_project(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} not found"
            )
        
        # Start background analysis
        background_tasks.add_task(
            _run_enhanced_analysis,
            project_id=project_id,
            project=project,
            enable_ai=request.enable_ai,
            max_files=request.max_files_for_ai,
            include_functions=request.include_function_explanations,
            include_classes=request.include_class_explanations,
            include_summaries=request.include_file_summaries,
        )
        
        # Estimate processing time based on project size
        estimated_time = _estimate_processing_time(project, request)
        
        return EnhancedAnalysisResponse(
            project_id=project_id,
            status="processing",
            message="Enhanced analysis started with AI integration",
            analysis_id=f"analysis_{project_id}",
            estimated_time_seconds=estimated_time,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start enhanced analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start analysis: {str(e)}"
        )


@router.get(
    "/{project_id}/analysis-with-ai",
    response_model=ProjectAnalysisWithAI,
    status_code=status.HTTP_200_OK,
    summary="Get enhanced analysis results",
    description="Retrieve the results of an enhanced analysis with AI insights",
    responses={
        200: {"description": "Analysis results retrieved successfully"},
        404: {"description": "Analysis not found"},
        500: {"description": "Internal server error"},
    }
)
async def get_enhanced_analysis(project_id: str) -> ProjectAnalysisWithAI:
    """
    Get enhanced analysis results for a project
    
    Returns the complete analysis including:
    - Code metrics and structure
    - AI-generated explanations and summaries
    - Key insights and recommendations
    - Prioritized files for review
    """
    try:
        # Load analysis result
        from app.utils.storage import load_analysis_result
        
        analysis = load_analysis_result(project_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Analysis for project {project_id} not found"
            )
        
        # Check if it's an enhanced analysis
        if not analysis.get("ai_enabled"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Enhanced analysis not available for project {project_id}. Run /analyze-with-ai first."
            )
        
        return ProjectAnalysisWithAI(**analysis)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve enhanced analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve analysis: {str(e)}"
        )


@router.get(
    "/ai/stats",
    response_model=AIProcessingStats,
    status_code=status.HTTP_200_OK,
    summary="Get AI processing statistics",
    description="Get statistics about AI processing performance",
)
async def get_ai_processing_stats() -> AIProcessingStats:
    """
    Get AI processing statistics
    
    Returns metrics about:
    - Total AI requests made
    - Success/failure rates
    - Cache hit rates
    - Processing times
    """
    try:
        integration_service = get_integration_service()
        return integration_service.get_processing_stats()
        
    except Exception as e:
        logger.error(f"Failed to get AI stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}"
        )


def _run_enhanced_analysis(
    project_id: str,
    project: Dict[str, Any],
    enable_ai: bool = True,
    max_files: int = 10,
    include_functions: bool = True,
    include_classes: bool = True,
    include_summaries: bool = True,
) -> None:
    """
    Run enhanced analysis in background
    
    This function performs the complete analysis workflow:
    1. Run standard code analysis
    2. Add AI insights if enabled
    3. Save results
    """
    try:
        logger.info(f"Starting enhanced analysis for project {project_id}")
        
        # Initialize analyzer
        analyzer = CodeAnalyzer()
        
        # Run base analysis
        repo_url = project.get("repository_url")
        if repo_url:
            analysis_result = analyzer.analyze_repository(repo_url, project_id)
        else:
            # For uploaded projects, analyze local directory
            local_path = project.get("local_path")
            if local_path:
                analysis_result = analyzer.analyze_local_directory(local_path, project_id)
            else:
                raise ValueError("No repository URL or local path found")
        
        # Check if base analysis succeeded
        if analysis_result.get("status") == "failed":
            logger.error(f"Base analysis failed: {analysis_result.get('error')}")
            save_analysis_result(project_id, analysis_result)
            return
        
        # Add AI insights if enabled
        if enable_ai:
            logger.info(f"Adding AI insights to analysis for project {project_id}")
            integration_service = get_integration_service()
            
            enhanced_result = integration_service.add_ai_explanations(
                analysis_result,
                max_files=max_files,
                include_functions=include_functions,
                include_classes=include_classes,
                include_summaries=include_summaries,
            )
        else:
            enhanced_result = {
                **analysis_result,
                "ai_enabled": False,
            }
        
        # Save enhanced result
        save_analysis_result(project_id, enhanced_result)
        
        logger.info(f"Enhanced analysis completed for project {project_id}")
        
    except Exception as e:
        logger.error(f"Enhanced analysis failed for project {project_id}: {e}")
        
        # Save error result
        error_result = {
            "project_id": project_id,
            "status": "failed",
            "error": str(e),
            "ai_enabled": enable_ai,
        }
        save_analysis_result(project_id, error_result)


def _estimate_processing_time(project: Dict[str, Any], request: EnhancedAnalysisRequest) -> int:
    """
    Estimate processing time based on project characteristics
    
    Args:
        project: Project data
        request: Analysis request
        
    Returns:
        Estimated time in seconds
    """
    # Base time for code analysis
    base_time = 30
    
    # Add time for AI processing if enabled
    if request.enable_ai:
        # Estimate ~5 seconds per file for AI processing
        ai_time = request.max_files_for_ai * 5
        
        # Add extra time for function/class explanations
        if request.include_function_explanations:
            ai_time += request.max_files_for_ai * 2
        if request.include_class_explanations:
            ai_time += request.max_files_for_ai * 2
        
        base_time += ai_time
    
    return base_time


# Made with Bob