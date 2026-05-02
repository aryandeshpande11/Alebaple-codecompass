"""
Simple file-based storage for development/PoC
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, cast
from datetime import datetime


class FileStorage:
    """Simple JSON file-based storage for projects and analysis results"""
    
    def __init__(self, storage_dir: str = "data"):
        """Initialize storage with a directory path"""
        self.storage_dir = Path(storage_dir)
        self.projects_file = self.storage_dir / "projects.json"
        self.analysis_file = self.storage_dir / "analysis.json"
        
        # Create storage directory if it doesn't exist
        self.storage_dir.mkdir(exist_ok=True)
        
        # Initialize storage files if they don't exist
        self._init_storage()
    
    def _init_storage(self):
        """Initialize storage files with empty data"""
        if not self.projects_file.exists():
            self._write_json(self.projects_file, {})
        
        if not self.analysis_file.exists():
            self._write_json(self.analysis_file, {})
    
    def _read_json(self, file_path: Path) -> Dict:
        """Read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write_json(self, file_path: Path, data: Dict):
        """Write JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    # Project operations
    def create_project(self, project_id: str, project_data: Dict) -> Dict:
        """Create a new project"""
        projects = self._read_json(self.projects_file)
        
        # Add timestamps
        now = datetime.utcnow().isoformat()
        project_data['id'] = project_id
        project_data['created_at'] = now
        project_data['updated_at'] = now
        project_data['status'] = 'pending'
        
        projects[project_id] = project_data
        self._write_json(self.projects_file, projects)
        
        return project_data
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """Get a project by ID"""
        projects = self._read_json(self.projects_file)
        return projects.get(project_id)
    
    def get_all_projects(self) -> List[Dict]:
        """Get all projects"""
        projects = self._read_json(self.projects_file)
        return list(projects.values())
    
    def update_project(self, project_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a project"""
        projects = self._read_json(self.projects_file)
        
        if project_id not in projects:
            return None
        
        # Update fields
        projects[project_id].update(update_data)
        projects[project_id]['updated_at'] = datetime.utcnow().isoformat()
        
        self._write_json(self.projects_file, projects)
        return cast(Dict[str, Any], projects[project_id])
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        projects = self._read_json(self.projects_file)
        
        if project_id in projects:
            del projects[project_id]
            self._write_json(self.projects_file, projects)
            
            # Also delete associated analysis
            self.delete_analysis(project_id)
            return True
        
        return False
    
    # Analysis operations
    def create_analysis(self, project_id: str, analysis_data: Dict) -> Dict:
        """Create or update analysis results"""
        analyses = self._read_json(self.analysis_file)
        
        analysis_data['project_id'] = project_id
        analysis_data['started_at'] = analysis_data.get('started_at', datetime.utcnow().isoformat())
        
        analyses[project_id] = analysis_data
        self._write_json(self.analysis_file, analyses)
        
        return analysis_data
    
    def get_analysis(self, project_id: str) -> Optional[Dict]:
        """Get analysis results for a project"""
        analyses = self._read_json(self.analysis_file)
        return analyses.get(project_id)
    
    def update_analysis(self, project_id: str, update_data: Dict) -> Optional[Dict]:
        """Update analysis results"""
        analyses = self._read_json(self.analysis_file)
        
        if project_id not in analyses:
            return None
        
        analyses[project_id].update(update_data)
        self._write_json(self.analysis_file, analyses)
        
        return analyses[project_id]
    
    def delete_analysis(self, project_id: str) -> bool:
        """Delete analysis results"""
        analyses = self._read_json(self.analysis_file)
        
        if project_id in analyses:
            del analyses[project_id]
            self._write_json(self.analysis_file, analyses)
            return True
        
        return False


# Global storage instance
storage = FileStorage()


# Helper functions for easier access
def load_project(project_id: str) -> Optional[Dict]:
    """Load a project by ID"""
    return storage.get_project(project_id)


def save_project(project_id: str, project_data: Dict) -> Dict:
    """Save or update a project"""
    existing = storage.get_project(project_id)
    if existing:
        return storage.update_project(project_id, project_data) or {}
    return storage.create_project(project_id, project_data)


def load_analysis_result(project_id: str) -> Optional[Dict]:
    """Load analysis results for a project"""
    return storage.get_analysis(project_id)


def save_analysis_result(project_id: str, analysis_data: Dict) -> Dict:
    """Save or update analysis results"""
    return storage.create_analysis(project_id, analysis_data)


def delete_project_data(project_id: str) -> bool:
    """Delete a project and its analysis"""
    return storage.delete_project(project_id)


# Made with Bob
