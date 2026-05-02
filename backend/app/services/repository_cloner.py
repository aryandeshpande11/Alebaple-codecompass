"""
Repository cloner service for handling Git repository operations.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional
from git import Repo, GitCommandError


class RepositoryCloner:
    """Service for cloning and managing Git repositories."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the repository cloner.
        
        Args:
            base_dir: Base directory for cloning repositories. 
                     If None, uses system temp directory.
        """
        self.base_dir = base_dir or tempfile.gettempdir()
        self.repos_dir = Path(self.base_dir) / "code_analysis_repos"
        self.repos_dir.mkdir(parents=True, exist_ok=True)
    
    def clone_repository(self, repo_url: str, project_id: str) -> Path:
        """
        Clone a Git repository.
        
        Args:
            repo_url: URL of the Git repository to clone
            project_id: Unique identifier for the project
            
        Returns:
            Path to the cloned repository
            
        Raises:
            ValueError: If the repository URL is invalid
            GitCommandError: If cloning fails
        """
        if not repo_url:
            raise ValueError("Repository URL cannot be empty")
        
        # Create project-specific directory
        project_dir = self.repos_dir / project_id
        
        # Remove existing directory if it exists
        if project_dir.exists():
            shutil.rmtree(project_dir)
        
        try:
            # Clone the repository
            Repo.clone_from(repo_url, project_dir, depth=1)
            return project_dir
        except GitCommandError as e:
            raise GitCommandError(f"Failed to clone repository: {str(e)}")
    
    def get_repository_path(self, project_id: str) -> Optional[Path]:
        """
        Get the path to a cloned repository.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Path to the repository if it exists, None otherwise
        """
        project_dir = self.repos_dir / project_id
        return project_dir if project_dir.exists() else None
    
    def delete_repository(self, project_id: str) -> bool:
        """
        Delete a cloned repository.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            True if deletion was successful, False otherwise
        """
        project_dir = self.repos_dir / project_id
        if project_dir.exists():
            try:
                shutil.rmtree(project_dir)
                return True
            except Exception:
                return False
        return False
    
    def list_source_files(self, project_id: str) -> list[Path]:
        """
        List all supported source code files in a cloned repository.
        Supports: Python (.py), Java (.java), JavaScript (.js, .jsx), TypeScript (.ts, .tsx)
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            List of paths to source files
        """
        project_dir = self.get_repository_path(project_id)
        if not project_dir:
            return []
        
        # Supported file extensions
        extensions = ['*.py', '*.java', '*.js', '*.jsx', '*.ts', '*.tsx']
        
        source_files = []
        for ext in extensions:
            for file_path in project_dir.rglob(ext):
                # Skip common ignore patterns
                if any(part in file_path.parts for part in [
                    '.venv', 'venv', '__pycache__', '.git', 'node_modules',
                    'build', 'dist', 'target', '.next', 'out'
                ]):
                    continue
                source_files.append(file_path)
        
        return source_files
    
    def list_python_files(self, project_id: str) -> list[Path]:
        """
        List all Python files in a cloned repository (backward compatibility).
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            List of paths to Python files
        """
        project_dir = self.get_repository_path(project_id)
        if not project_dir:
            return []
        
        python_files = []
        for file_path in project_dir.rglob("*.py"):
            # Skip virtual environments and common ignore patterns
            if any(part in file_path.parts for part in ['.venv', 'venv', '__pycache__', '.git']):
                continue
            python_files.append(file_path)
        
        return python_files
    
    def get_repository_info(self, project_id: str) -> dict:
        """
        Get information about a cloned repository.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dictionary containing repository information
        """
        project_dir = self.get_repository_path(project_id)
        if not project_dir:
            return {}
        
        try:
            repo = Repo(project_dir)
            return {
                "path": str(project_dir),
                "branch": repo.active_branch.name,
                "commit": repo.head.commit.hexsha[:7],
                "commit_message": repo.head.commit.message.strip(),
                "author": str(repo.head.commit.author),
                "commit_date": repo.head.commit.committed_datetime.isoformat(),
            }
        except Exception:
            return {"path": str(project_dir)}

# Made with Bob
