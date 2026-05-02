"""
Metrics calculator service for analyzing code complexity and quality.
"""

from pathlib import Path
from typing import Any
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
from radon.raw import analyze


class MetricsCalculator:
    """Service for calculating code metrics."""
    
    def __init__(self):
        """Initialize the metrics calculator."""
        pass
    
    def calculate_file_metrics(self, file_path: Path) -> dict[str, Any]:
        """
        Calculate metrics for a single Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary containing calculated metrics
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Raw metrics (LOC, comments, etc.)
            raw_metrics = analyze(source_code)
            
            # Cyclomatic complexity
            complexity_results = cc_visit(source_code)
            
            # Maintainability index
            try:
                mi_score = mi_visit(source_code, multi=True)
            except Exception:
                mi_score = None
            
            # Halstead metrics
            try:
                halstead = h_visit(source_code)
            except Exception:
                halstead = None
            
            return {
                "file_path": str(file_path),
                "raw_metrics": {
                    "loc": raw_metrics.loc,  # Lines of code
                    "lloc": raw_metrics.lloc,  # Logical lines of code
                    "sloc": raw_metrics.sloc,  # Source lines of code
                    "comments": raw_metrics.comments,
                    "multi": raw_metrics.multi,  # Multi-line strings
                    "blank": raw_metrics.blank,
                    "single_comments": raw_metrics.single_comments,
                },
                "complexity": self._format_complexity(complexity_results),
                "maintainability_index": mi_score,
                "halstead": self._format_halstead(halstead) if halstead else None,
            }
        except Exception as e:
            return {
                "file_path": str(file_path),
                "error": f"Metrics calculation error: {str(e)}",
                "raw_metrics": {},
                "complexity": [],
                "maintainability_index": None,
                "halstead": None,
            }
    
    def _format_complexity(self, complexity_results: list) -> list[dict[str, Any]]:
        """Format complexity results."""
        formatted = []
        for result in complexity_results:
            formatted.append({
                "name": result.name,
                "type": result.letter,  # F=function, M=method, C=class
                "complexity": result.complexity,
                "line_number": result.lineno,
                "col_offset": result.col_offset,
                "rank": self._get_complexity_rank(result.complexity),
            })
        return formatted
    
    def _get_complexity_rank(self, complexity: int) -> str:
        """Get complexity rank based on cyclomatic complexity."""
        if complexity <= 5:
            return "A"  # Low risk
        elif complexity <= 10:
            return "B"  # Moderate risk
        elif complexity <= 20:
            return "C"  # High risk
        elif complexity <= 30:
            return "D"  # Very high risk
        else:
            return "F"  # Extreme risk
    
    def _format_halstead(self, halstead: Any) -> dict[str, Any]:
        """Format Halstead metrics."""
        if not halstead:
            return {}
        
        return {
            "h1": halstead.h1,  # Number of distinct operators
            "h2": halstead.h2,  # Number of distinct operands
            "N1": halstead.N1,  # Total number of operators
            "N2": halstead.N2,  # Total number of operands
            "vocabulary": halstead.vocabulary,
            "length": halstead.length,
            "calculated_length": halstead.calculated_length,
            "volume": halstead.volume,
            "difficulty": halstead.difficulty,
            "effort": halstead.effort,
            "time": halstead.time,
            "bugs": halstead.bugs,
        }
    
    def calculate_project_metrics(self, file_metrics: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Calculate aggregate metrics for an entire project.
        
        Args:
            file_metrics: List of metrics for individual files
            
        Returns:
            Dictionary containing project-wide metrics
        """
        total_loc = 0
        total_lloc = 0
        total_sloc = 0
        total_comments = 0
        total_blank = 0
        total_files = len(file_metrics)
        files_with_errors = 0
        
        all_complexity = []
        maintainability_scores = []
        
        for metrics in file_metrics:
            if "error" in metrics:
                files_with_errors += 1
                continue
            
            raw = metrics.get("raw_metrics", {})
            total_loc += raw.get("loc", 0)
            total_lloc += raw.get("lloc", 0)
            total_sloc += raw.get("sloc", 0)
            total_comments += raw.get("comments", 0)
            total_blank += raw.get("blank", 0)
            
            complexity = metrics.get("complexity", [])
            all_complexity.extend([c["complexity"] for c in complexity])
            
            mi = metrics.get("maintainability_index")
            if mi is not None:
                maintainability_scores.append(mi)
        
        # Calculate averages
        avg_complexity = sum(all_complexity) / len(all_complexity) if all_complexity else 0
        avg_maintainability = sum(maintainability_scores) / len(maintainability_scores) if maintainability_scores else 0
        
        # Count high complexity functions
        high_complexity_count = sum(1 for c in all_complexity if c > 10)
        
        return {
            "total_files": total_files,
            "files_with_errors": files_with_errors,
            "total_loc": total_loc,
            "total_lloc": total_lloc,
            "total_sloc": total_sloc,
            "total_comments": total_comments,
            "total_blank": total_blank,
            "comment_ratio": total_comments / total_sloc if total_sloc > 0 else 0,
            "average_complexity": round(avg_complexity, 2),
            "max_complexity": max(all_complexity) if all_complexity else 0,
            "high_complexity_count": high_complexity_count,
            "average_maintainability": round(avg_maintainability, 2),
            "complexity_distribution": self._get_complexity_distribution(all_complexity),
        }
    
    def _get_complexity_distribution(self, complexities: list[int]) -> dict[str, int]:
        """Get distribution of complexity ranks."""
        distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for complexity in complexities:
            rank = self._get_complexity_rank(complexity)
            distribution[rank] += 1
        return distribution

# Made with Bob
