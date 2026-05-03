"""
Main code analyzer service that orchestrates all analysis components.
Supports multiple programming languages: Python, Java, JavaScript, TypeScript
"""

from pathlib import Path
from typing import Any
from datetime import datetime

from .repository_cloner import RepositoryCloner
from .universal_parser import UniversalParser
from .metrics_calculator import MetricsCalculator


class CodeAnalyzer:
    """Main service for analyzing code repositories in multiple languages."""
    
    def __init__(self):
        """Initialize the code analyzer with all sub-services."""
        self.cloner = RepositoryCloner()
        self.parser = UniversalParser()
        self.metrics = MetricsCalculator()
    
    def analyze_repository(self, repo_url: str, project_id: str) -> dict[str, Any]:
        """
        Analyze a Git repository completely.
        
        Args:
            repo_url: URL of the Git repository
            project_id: Unique identifier for the project
            
        Returns:
            Dictionary containing complete analysis results
        """
        analysis_start = datetime.utcnow()
        
        try:
            # Step 1: Clone the repository
            repo_path = self.cloner.clone_repository(repo_url, project_id)
            repo_info = self.cloner.get_repository_info(project_id)
            
            # Step 2: Get all source files (Python, Java, JS, TS)
            source_files = self.cloner.list_source_files(project_id)
            
            if not source_files:
                return {
                    "project_id": project_id,
                    "status": "completed",
                    "error": "No supported source files found in repository",
                    "repository_info": repo_info,
                    "analysis_timestamp": analysis_start.isoformat(),
                }
            
            # Step 3: Parse all files
            parsed_files = []
            for file_path in source_files:
                parsed = self.parser.parse_file(file_path)
                parsed_files.append(parsed)
            
            # Step 4: Calculate metrics for all files (Python only for now)
            file_metrics = []
            for file_path in source_files:
                # Only calculate radon metrics for Python files
                if file_path.suffix == '.py':
                    metrics = self.metrics.calculate_file_metrics(file_path)
                else:
                    # Basic metrics for non-Python files
                    metrics = self._calculate_basic_metrics(file_path)
                file_metrics.append(metrics)
            
            # Step 5: Calculate project-wide metrics
            project_metrics = self.metrics.calculate_project_metrics(file_metrics)
            
            # Step 6: Build dependency graph
            dependencies = self._build_dependency_graph(parsed_files)
            
            # Step 7: Generate file structure
            file_structure = self._build_file_structure(source_files, repo_path)
            
            # Step 8: Get language distribution
            language_stats = self._get_language_stats(parsed_files)
            
            analysis_end = datetime.utcnow()
            duration = (analysis_end - analysis_start).total_seconds()
            
            return {
                "project_id": project_id,
                "status": "completed",
                "repository_info": repo_info,
                "analysis_timestamp": analysis_start.isoformat(),
                "analysis_duration_seconds": duration,
                "summary": {
                    "total_files": len(source_files),
                    "languages": language_stats,
                    "total_classes": sum(len(p.get("classes", [])) for p in parsed_files),
                    "total_functions": sum(len(p.get("functions", [])) for p in parsed_files),
                    "total_imports": sum(len(p.get("imports", [])) for p in parsed_files),
                    **project_metrics,
                },
                "files": self._combine_file_data(parsed_files, file_metrics),
                "dependencies": dependencies,
                "file_structure": file_structure,
            }
            
        except Exception as e:
            return {
                "project_id": project_id,
                "status": "failed",
                "error": str(e),
                "analysis_timestamp": analysis_start.isoformat(),
            }
    
    def analyze_local_directory(self, directory_path: str, project_id: str) -> dict[str, Any]:
        """
        Analyze a local directory (for uploaded code).
        
        Args:
            directory_path: Path to the local directory
            project_id: Unique identifier for the project
            
        Returns:
            Dictionary containing complete analysis results
        """
        analysis_start = datetime.utcnow()
        
        try:
            dir_path = Path(directory_path)
            if not dir_path.exists():
                raise ValueError(f"Directory does not exist: {directory_path}")
            
            # Get all source files (Python, Java, JS, TS)
            extensions = ['*.py', '*.java', '*.js', '*.jsx', '*.ts', '*.tsx']
            source_files = []
            for ext in extensions:
                for file_path in dir_path.rglob(ext):
                    if not any(part in file_path.parts for part in [
                        '.venv', 'venv', '__pycache__', 'node_modules', 'build', 'dist'
                    ]):
                        source_files.append(file_path)
            
            if not source_files:
                return {
                    "project_id": project_id,
                    "status": "completed",
                    "error": "No supported source files found in directory",
                    "analysis_timestamp": analysis_start.isoformat(),
                }
            
            # Parse all files
            parsed_files = []
            for file_path in source_files:
                parsed = self.parser.parse_file(file_path)
                parsed_files.append(parsed)
            
            # Calculate metrics
            file_metrics = []
            for file_path in source_files:
                if file_path.suffix == '.py':
                    metrics = self.metrics.calculate_file_metrics(file_path)
                else:
                    metrics = self._calculate_basic_metrics(file_path)
                file_metrics.append(metrics)
            
            project_metrics = self.metrics.calculate_project_metrics(file_metrics)
            dependencies = self._build_dependency_graph(parsed_files)
            file_structure = self._build_file_structure(source_files, dir_path)
            language_stats = self._get_language_stats(parsed_files)
            
            analysis_end = datetime.utcnow()
            duration = (analysis_end - analysis_start).total_seconds()
            
            return {
                "project_id": project_id,
                "status": "completed",
                "analysis_timestamp": analysis_start.isoformat(),
                "analysis_duration_seconds": duration,
                "summary": {
                    "total_files": len(source_files),
                    "languages": language_stats,
                    "total_classes": sum(len(p.get("classes", [])) for p in parsed_files),
                    "total_functions": sum(len(p.get("functions", [])) for p in parsed_files),
                    "total_imports": sum(len(p.get("imports", [])) for p in parsed_files),
                    **project_metrics,
                },
                "files": self._combine_file_data(parsed_files, file_metrics),
                "dependencies": dependencies,
                "file_structure": file_structure,
            }
            
        except Exception as e:
            return {
                "project_id": project_id,
                "status": "failed",
                "error": str(e),
                "analysis_timestamp": analysis_start.isoformat(),
            }
    
    def _combine_file_data(
        self,
        parsed_files: list[dict[str, Any]],
        file_metrics: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Combine parsed data and metrics for each file."""
        combined = []
        for parsed, metrics in zip(parsed_files, file_metrics):
            # Read file content
            file_path = parsed.get("file_path", "")
            content = ""
            language = parsed.get("language", "plaintext")
            
            try:
                if file_path:
                    from pathlib import Path
                    path_obj = Path(file_path)
                    if path_obj.exists():
                        with open(path_obj, 'r', encoding='utf-8') as f:
                            content = f.read()
            except Exception as e:
                content = f"// Error reading file: {str(e)}"
            
            combined.append({
                "file_path": file_path,
                "content": content,
                "language": language,
                "has_error": "error" in parsed or "error" in metrics,
                "error": parsed.get("error") or metrics.get("error"),
                "structure": {
                    "classes": parsed.get("classes", []),
                    "functions": parsed.get("functions", []),
                    "imports": parsed.get("imports", []),
                    "constants": parsed.get("constants", []),
                    "docstring": parsed.get("docstring"),
                },
                "metrics": {
                    "raw": metrics.get("raw_metrics", {}),
                    "complexity": metrics.get("complexity", []),
                    "maintainability_index": metrics.get("maintainability_index"),
                    "halstead": metrics.get("halstead"),
                },
            })
        return combined
    
    def _build_dependency_graph(self, parsed_files: list[dict[str, Any]]) -> dict[str, Any]:
        """Build a dependency graph from parsed files."""
        # Extract all imports
        all_imports = {}
        for parsed in parsed_files:
            file_path = parsed["file_path"]
            imports = parsed.get("imports", [])
            
            # Get unique modules imported
            modules = set()
            for imp in imports:
                if imp["type"] == "import":
                    modules.add(imp["module"])
                elif imp["type"] == "from_import":
                    modules.add(imp["module"])
            
            all_imports[file_path] = list(modules)
        
        # Count import frequencies
        import_counts = {}
        for imports in all_imports.values():
            for module in imports:
                import_counts[module] = import_counts.get(module, 0) + 1
        
        # Get top imports
        top_imports = sorted(import_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        
        return {
            "file_imports": all_imports,
            "import_counts": import_counts,
            "top_imports": [{"module": mod, "count": count} for mod, count in top_imports],
            "total_unique_imports": len(import_counts),
        }
    
    def _build_file_structure(self, python_files: list[Path], base_path: Path) -> dict[str, Any]:
        """Build a hierarchical file structure."""
        structure = {}
        
        for file_path in python_files:
            try:
                relative_path = file_path.relative_to(base_path)
                parts = relative_path.parts
                
                current = structure
                for i, part in enumerate(parts[:-1]):
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                
                # Add file
                current[parts[-1]] = {
                    "type": "file",
                    "path": str(relative_path),
                    "size": file_path.stat().st_size,
                }
            except ValueError:
                # File is not relative to base_path
                continue
        
        return structure
    
    def get_file_analysis(self, project_id: str, file_path: str) -> dict[str, Any]:
        """
        Get detailed analysis for a specific file.
        
        Args:
            project_id: Unique identifier for the project
            file_path: Path to the file (relative to project root)
            
        Returns:
            Dictionary containing file analysis
        """
        repo_path = self.cloner.get_repository_path(project_id)
        if not repo_path:
            return {"error": "Project not found"}
        
        full_path = repo_path / file_path
        if not full_path.exists():
            return {"error": "File not found"}
        
        parsed = self.parser.parse_file(full_path)
        metrics = self.metrics.calculate_file_metrics(full_path)
        
        return {
            "file_path": file_path,
            "structure": parsed,
            "metrics": metrics,
        }

# Made with Bob

    
    def _calculate_basic_metrics(self, file_path: Path) -> dict[str, Any]:
        """Calculate basic metrics for non-Python files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            loc = len(lines)
            blank = sum(1 for line in lines if line.strip() == '')
            sloc = loc - blank
            
            return {
                "file_path": str(file_path),
                "raw_metrics": {
                    "loc": loc,
                    "lloc": sloc,
                    "sloc": sloc,
                    "comments": 0,
                    "multi": 0,
                    "blank": blank,
                    "single_comments": 0,
                },
                "complexity": [],
                "maintainability_index": None,
                "halstead": None,
            }
        except Exception:
            return {
                "file_path": str(file_path),
                "error": "Failed to calculate metrics",
                "raw_metrics": {},
                "complexity": [],
                "maintainability_index": None,
                "halstead": None,
            }
    
    def _get_language_stats(self, parsed_files: list[dict[str, Any]]) -> dict[str, int]:
        """Get statistics about languages used in the project."""
        language_counts = {}
        for parsed in parsed_files:
            lang = parsed.get("language", "unknown")
            language_counts[lang] = language_counts.get(lang, 0) + 1
        return language_counts
