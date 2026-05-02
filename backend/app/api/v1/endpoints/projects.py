"""
Project management API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    ProjectList
)
from app.utils.storage import storage
from app.utils.id_generator import generate_id

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    """
    Create a new project
    
    - **name**: Project name (required)
    - **github_url**: GitHub repository URL (optional)
    - **description**: Project description (optional)
    """
    try:
        # Generate unique project ID
        project_id = generate_id("proj")
        
        # Prepare project data
        project_data = project.model_dump()
        
        # Convert HttpUrl to string if present
        if project_data.get('github_url'):
            project_data['github_url'] = str(project_data['github_url'])
        
        # Create project in storage
        created_project = storage.create_project(project_id, project_data)
        
        return ProjectResponse(**created_project)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create project: {str(e)}"
        )


@router.get("/", response_model=ProjectList)
async def list_projects():
    """
    Get all projects
    
    Returns a list of all projects with their metadata
    """
    try:
        projects = storage.get_all_projects()
        
        return ProjectList(
            projects=[ProjectResponse(**p) for p in projects],
            total=len(projects)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve projects: {str(e)}"
        )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    Get a specific project by ID
    
    - **project_id**: Unique project identifier
    """
    project = storage.get_project(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    return ProjectResponse(**project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: str, project_update: ProjectUpdate):
    """
    Update a project
    
    - **project_id**: Unique project identifier
    - **name**: New project name (optional)
    - **description**: New project description (optional)
    """
    # Check if project exists
    existing_project = storage.get_project(project_id)
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    # Prepare update data (only include non-None fields)
    update_data = project_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    try:
        updated_project = storage.update_project(project_id, update_data)
        if not updated_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID '{project_id}' not found"
            )
        return ProjectResponse(**updated_project)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update project: {str(e)}"
        )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str):
    """
    Delete a project
    
    - **project_id**: Unique project identifier
    
    This will also delete all associated analysis results
    """
    success = storage.delete_project(project_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID '{project_id}' not found"
        )
    
    return None

# Made with Bob
