"""
Analysis AI Integration Service
Integrates AI explanations with code analysis results
"""

import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from app.services.ai_service import get_ai_service
from app.utils.ai_helpers import AIHelpers
from app.schemas.analysis_enhanced import (
    AIInsight,
    FunctionWithAI,
    ClassWithAI,
    FileAnalysisWithAI,
    AIProcessingStats,
)

logger = logging.getLogger(__name__)


class AnalysisAIIntegration:
    """Service for integrating AI insights with code analysis"""
    
    def __init__(self):
        """Initialize the integration service"""
        self.ai_service = get_ai_service()
        self.helpers = AIHelpers()
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "cached_responses": 0,
            "total_processing_time": 0.0,
        }
    
    def add_ai_explanations(
        self,
        analysis_result: Dict[str, Any],
        max_files: int = 10,
        include_functions: bool = True,
        include_classes: bool = True,
        include_summaries: bool = True,
    ) -> Dict[str, Any]:
        """
        Add AI explanations to analysis results
        
        Args:
            analysis_result: Base analysis result from code analyzer
            max_files: Maximum number of files to process with AI
            include_functions: Include function explanations
            include_classes: Include class explanations
            include_summaries: Include file summaries
            
        Returns:
            Enhanced analysis result with AI insights
        """
        start_time = time.time()
        
        try:
            # Extract files from analysis
            files = analysis_result.get("files", [])
            
            if not files:
                logger.warning("No files found in analysis result")
                return analysis_result
            
            # Prioritize files for AI analysis
            prioritized = self.helpers.prioritize_files_for_ai(files, max_files)
            
            logger.info(f"Processing {len(prioritized)} files with AI (out of {len(files)} total)")
            
            # Process each prioritized file
            enhanced_files = []
            ai_errors = []
            
            for priority_item in prioritized:
                file_data = priority_item["data"]
                file_path = file_data.get("file_path", "")
                
                try:
                    enhanced_file = self._process_file_with_ai(
                        file_data,
                        include_functions=include_functions,
                        include_classes=include_classes,
                        include_summaries=include_summaries,
                    )
                    enhanced_files.append(enhanced_file)
                    
                except Exception as e:
                    logger.error(f"Failed to process file {file_path} with AI: {e}")
                    ai_errors.append(f"{file_path}: {str(e)}")
                    # Add file without AI enhancements
                    enhanced_files.append(file_data)
            
            # Add remaining files without AI processing
            processed_paths = {f.get("file_path") for f in enhanced_files}
            for file_data in files:
                if file_data.get("file_path") not in processed_paths:
                    enhanced_files.append(file_data)
            
            # Generate project-level insights
            key_insights = self._generate_project_insights(enhanced_files)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            self.stats["total_processing_time"] += processing_time
            
            # Build enhanced result
            enhanced_result = {
                **analysis_result,
                "files": enhanced_files,
                "ai_enabled": True,
                "ai_summary": self._generate_project_summary(analysis_result, enhanced_files),
                "key_insights": key_insights,
                "priority_files": [
                    {
                        "file_path": p["file_path"],
                        "priority_score": p["priority_score"],
                        "reasons": p["reasons"],
                    }
                    for p in prioritized
                ],
                "ai_processing_time": round(processing_time, 2),
                "ai_errors": ai_errors,
            }
            
            return enhanced_result
            
        except Exception as e:
            logger.error(f"Failed to add AI explanations: {e}")
            # Return original result on error
            return {
                **analysis_result,
                "ai_enabled": False,
                "ai_errors": [str(e)],
            }
    
    def _process_file_with_ai(
        self,
        file_data: Dict[str, Any],
        include_functions: bool = True,
        include_classes: bool = True,
        include_summaries: bool = True,
    ) -> Dict[str, Any]:
        """Process a single file with AI"""
        file_path = file_data.get("file_path", "")
        structure = file_data.get("structure", {})
        
        # Detect language from file extension
        language = self._detect_language(file_path)
        
        enhanced_file = {**file_data}
        
        # Add file summary if requested
        if include_summaries:
            try:
                summary = self._get_file_summary(file_path, language)
                if summary:
                    enhanced_file["ai_summary"] = summary
            except Exception as e:
                logger.warning(f"Failed to get file summary for {file_path}: {e}")
        
        # Process important functions
        if include_functions:
            try:
                important_functions = self.helpers.detect_important_functions(structure)
                enhanced_functions = []
                
                for func in important_functions[:5]:  # Limit to top 5
                    func_with_ai = self._add_function_explanation(
                        func, file_path, language
                    )
                    if func_with_ai:
                        enhanced_functions.append(func_with_ai)
                
                if enhanced_functions:
                    enhanced_file["important_functions"] = enhanced_functions
                    
            except Exception as e:
                logger.warning(f"Failed to process functions for {file_path}: {e}")
        
        # Process important classes
        if include_classes:
            try:
                important_classes = self.helpers.detect_important_classes(structure)
                enhanced_classes = []
                
                for cls in important_classes[:5]:  # Limit to top 5
                    cls_with_ai = self._add_class_explanation(
                        cls, file_path, language
                    )
                    if cls_with_ai:
                        enhanced_classes.append(cls_with_ai)
                
                if enhanced_classes:
                    enhanced_file["important_classes"] = enhanced_classes
                    
            except Exception as e:
                logger.warning(f"Failed to process classes for {file_path}: {e}")
        
        return enhanced_file
    
    def _get_file_summary(self, file_path: str, language: str) -> Optional[Dict[str, Any]]:
        """Get AI summary for a file"""
        try:
            # Read file content
            path = Path(file_path)
            if not path.exists():
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Truncate if too large
            content, was_truncated = self.helpers.truncate_code_for_context(content)
            
            # Get AI summary
            self.stats["total_requests"] += 1
            result = self.ai_service.summarize_file(content, language, str(file_path))
            
            if "error" in result:
                self.stats["failed_requests"] += 1
                return None
            
            self.stats["successful_requests"] += 1
            if result.get("from_cache"):
                self.stats["cached_responses"] += 1
            
            return {
                "type": "summary",
                "content": result.get("summary", ""),
                "language": language,
                "timestamp": result.get("timestamp", ""),
                "model": result.get("model", ""),
                "from_cache": result.get("from_cache", False),
            }
            
        except Exception as e:
            logger.error(f"Failed to get file summary: {e}")
            self.stats["failed_requests"] += 1
            return None
    
    def _add_function_explanation(
        self,
        func_info: Dict[str, Any],
        file_path: str,
        language: str
    ) -> Optional[Dict[str, Any]]:
        """Add AI explanation to a function"""
        try:
            # Read file and extract function code
            path = Path(file_path)
            if not path.exists():
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            func_name = func_info.get("name", "")
            func_code = self.helpers.extract_function_snippet(content, func_name, language)
            
            if not func_code:
                # Use a placeholder if extraction fails
                func_code = f"# Function: {func_name}\n# (code extraction failed)"
            
            # Get AI explanation
            self.stats["total_requests"] += 1
            result = self.ai_service.explain_code(func_code, language)
            
            if "error" in result:
                self.stats["failed_requests"] += 1
                return {**func_info}
            
            self.stats["successful_requests"] += 1
            if result.get("from_cache"):
                self.stats["cached_responses"] += 1
            
            return {
                **func_info,
                "ai_explanation": {
                    "type": "explanation",
                    "content": result.get("explanation", ""),
                    "language": language,
                    "timestamp": result.get("timestamp", ""),
                    "model": result.get("model", ""),
                    "from_cache": result.get("from_cache", False),
                },
            }
            
        except Exception as e:
            logger.error(f"Failed to add function explanation: {e}")
            self.stats["failed_requests"] += 1
            return {**func_info}
    
    def _add_class_explanation(
        self,
        class_info: Dict[str, Any],
        file_path: str,
        language: str
    ) -> Optional[Dict[str, Any]]:
        """Add AI explanation to a class"""
        try:
            # Read file and extract class code
            path = Path(file_path)
            if not path.exists():
                return None
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            class_name = class_info.get("name", "")
            class_code = self.helpers.extract_class_snippet(content, class_name, language)
            
            if not class_code:
                # Use a placeholder if extraction fails
                class_code = f"# Class: {class_name}\n# (code extraction failed)"
            
            # Truncate if too large
            class_code, _ = self.helpers.truncate_code_for_context(class_code)
            
            # Get AI explanation
            self.stats["total_requests"] += 1
            result = self.ai_service.explain_code(class_code, language)
            
            if "error" in result:
                self.stats["failed_requests"] += 1
                return {**class_info}
            
            self.stats["successful_requests"] += 1
            if result.get("from_cache"):
                self.stats["cached_responses"] += 1
            
            return {
                **class_info,
                "ai_explanation": {
                    "type": "explanation",
                    "content": result.get("explanation", ""),
                    "language": language,
                    "timestamp": result.get("timestamp", ""),
                    "model": result.get("model", ""),
                    "from_cache": result.get("from_cache", False),
                },
            }
            
        except Exception as e:
            logger.error(f"Failed to add class explanation: {e}")
            self.stats["failed_requests"] += 1
            return {**class_info}
    
    def _generate_project_insights(self, files: List[Dict[str, Any]]) -> List[str]:
        """Generate key insights from analyzed files"""
        insights = []
        
        # Analyze complexity
        high_complexity_files = [
            f for f in files
            if f.get("metrics", {}).get("complexity", [])
            and any(c.get("complexity", 0) > 10 for c in f["metrics"]["complexity"])
        ]
        
        if high_complexity_files:
            insights.append(
                f"Found {len(high_complexity_files)} file(s) with high complexity functions - consider refactoring"
            )
        
        # Analyze maintainability
        low_maintainability = [
            f for f in files
            if f.get("metrics", {}).get("maintainability_index")
            and f["metrics"]["maintainability_index"] < 50
        ]
        
        if low_maintainability:
            insights.append(
                f"{len(low_maintainability)} file(s) have low maintainability index - review for improvements"
            )
        
        # Analyze documentation
        undocumented_functions = sum(
            1 for f in files
            for func in f.get("structure", {}).get("functions", [])
            if not func.get("docstring")
        )
        
        if undocumented_functions > 5:
            insights.append(
                f"{undocumented_functions} functions lack documentation - add docstrings for better clarity"
            )
        
        # Analyze AI-enhanced files
        ai_enhanced = [f for f in files if "ai_summary" in f or "important_functions" in f]
        if ai_enhanced:
            insights.append(
                f"AI analysis completed for {len(ai_enhanced)} priority files with detailed explanations"
            )
        
        return insights
    
    def _generate_project_summary(
        self,
        analysis_result: Dict[str, Any],
        enhanced_files: List[Dict[str, Any]]
    ) -> str:
        """Generate overall project summary"""
        summary = analysis_result.get("summary", {})
        
        total_files = summary.get("total_files", 0)
        languages = summary.get("languages", {})
        total_classes = summary.get("total_classes", 0)
        total_functions = summary.get("total_functions", 0)
        
        lang_str = ", ".join(f"{k} ({v})" for k, v in languages.items())
        
        summary_text = f"""This project contains {total_files} source files across multiple languages: {lang_str}. 
The codebase includes {total_classes} classes and {total_functions} functions. 
AI analysis has been performed on the most important files to provide detailed insights and explanations."""
        
        return summary_text
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        
        language_map = {
            ".py": "python",
            ".java": "java",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
        }
        
        return language_map.get(ext, "unknown")
    
    def get_processing_stats(self) -> AIProcessingStats:
        """Get AI processing statistics"""
        avg_time = (
            self.stats["total_processing_time"] / self.stats["total_requests"]
            if self.stats["total_requests"] > 0
            else 0
        )
        
        return AIProcessingStats(
            total_requests=self.stats["total_requests"],
            successful_requests=self.stats["successful_requests"],
            failed_requests=self.stats["failed_requests"],
            cached_responses=self.stats["cached_responses"],
            total_processing_time=round(self.stats["total_processing_time"], 2),
            average_response_time=round(avg_time, 2),
        )


# Global service instance
_integration_service: Optional[AnalysisAIIntegration] = None


def get_integration_service() -> AnalysisAIIntegration:
    """Get or create the global integration service instance"""
    global _integration_service
    if _integration_service is None:
        _integration_service = AnalysisAIIntegration()
    return _integration_service


# Made with Bob