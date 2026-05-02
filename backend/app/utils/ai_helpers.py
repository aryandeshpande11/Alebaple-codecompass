"""
AI Helper Utilities
Functions for code snippet extraction, complexity analysis, and token optimization
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class AIHelpers:
    """Helper functions for AI integration with code analysis"""
    
    @staticmethod
    def extract_function_snippet(code: str, function_name: str, language: str) -> Optional[str]:
        """
        Extract a specific function from code
        
        Args:
            code: Full code content
            function_name: Name of the function to extract
            language: Programming language
            
        Returns:
            Function code snippet or None if not found
        """
        if language == "python":
            # Match Python function definition
            pattern = rf'^def\s+{re.escape(function_name)}\s*\([^)]*\):.*?(?=\n(?:def\s|class\s|\Z))'
            match = re.search(pattern, code, re.MULTILINE | re.DOTALL)
            return match.group(0) if match else None
            
        elif language in ["javascript", "typescript"]:
            # Match JS/TS function definition (multiple styles)
            patterns = [
                rf'function\s+{re.escape(function_name)}\s*\([^)]*\)\s*{{[^}}]*}}',
                rf'const\s+{re.escape(function_name)}\s*=\s*\([^)]*\)\s*=>\s*{{[^}}]*}}',
                rf'const\s+{re.escape(function_name)}\s*=\s*function\s*\([^)]*\)\s*{{[^}}]*}}',
            ]
            for pattern in patterns:
                match = re.search(pattern, code, re.DOTALL)
                if match:
                    return match.group(0)
            return None
            
        elif language == "java":
            # Match Java method definition
            pattern = rf'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+{re.escape(function_name)}\s*\([^)]*\)\s*{{[^}}]*}}'
            match = re.search(pattern, code, re.DOTALL)
            return match.group(0) if match else None
            
        return None
    
    @staticmethod
    def extract_class_snippet(code: str, class_name: str, language: str) -> Optional[str]:
        """
        Extract a specific class from code
        
        Args:
            code: Full code content
            class_name: Name of the class to extract
            language: Programming language
            
        Returns:
            Class code snippet or None if not found
        """
        if language == "python":
            # Match Python class definition
            pattern = rf'^class\s+{re.escape(class_name)}\s*[:\(].*?(?=\n(?:class\s|def\s|\Z))'
            match = re.search(pattern, code, re.MULTILINE | re.DOTALL)
            return match.group(0) if match else None
            
        elif language in ["javascript", "typescript"]:
            # Match JS/TS class definition
            pattern = rf'class\s+{re.escape(class_name)}\s*(?:extends\s+\w+)?\s*{{[^}}]*}}'
            match = re.search(pattern, code, re.DOTALL)
            return match.group(0) if match else None
            
        elif language == "java":
            # Match Java class definition
            pattern = rf'(?:public|private)?\s*class\s+{re.escape(class_name)}\s*(?:extends\s+\w+)?(?:implements\s+[\w,\s]+)?\s*{{[^}}]*}}'
            match = re.search(pattern, code, re.DOTALL)
            return match.group(0) if match else None
            
        return None
    
    @staticmethod
    def detect_important_functions(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect important functions based on complexity and other metrics
        
        Args:
            parsed_data: Parsed file data from code analyzer
            
        Returns:
            List of important functions with metadata
        """
        functions = parsed_data.get("functions", [])
        important = []
        
        for func in functions:
            importance_score = 0
            reasons = []
            
            # Check complexity
            complexity = func.get("complexity", 0)
            if complexity > 10:
                importance_score += 3
                reasons.append("high_complexity")
            elif complexity > 5:
                importance_score += 2
                reasons.append("moderate_complexity")
            
            # Check if it's a public/exported function
            name = func.get("name", "")
            if not name.startswith("_"):
                importance_score += 1
                reasons.append("public_function")
            
            # Check docstring presence
            if func.get("docstring"):
                importance_score += 1
                reasons.append("documented")
            
            # Check number of arguments
            args_count = len(func.get("args", []))
            if args_count > 3:
                importance_score += 1
                reasons.append("many_parameters")
            
            if importance_score >= 2:
                important.append({
                    "name": name,
                    "line_number": func.get("line_number", 0),
                    "complexity": complexity,
                    "importance_score": importance_score,
                    "reasons": reasons,
                    "args": func.get("args", []),
                    "docstring": func.get("docstring"),
                })
        
        # Sort by importance score
        important.sort(key=lambda x: x["importance_score"], reverse=True)
        
        return important
    
    @staticmethod
    def detect_important_classes(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect important classes based on methods and structure
        
        Args:
            parsed_data: Parsed file data from code analyzer
            
        Returns:
            List of important classes with metadata
        """
        classes = parsed_data.get("classes", [])
        important = []
        
        for cls in classes:
            importance_score = 0
            reasons = []
            
            # Check number of methods
            methods_count = len(cls.get("methods", []))
            if methods_count > 5:
                importance_score += 3
                reasons.append("many_methods")
            elif methods_count > 2:
                importance_score += 2
                reasons.append("moderate_methods")
            
            # Check if it's a public class
            name = cls.get("name", "")
            if not name.startswith("_"):
                importance_score += 1
                reasons.append("public_class")
            
            # Check docstring presence
            if cls.get("docstring"):
                importance_score += 1
                reasons.append("documented")
            
            # Check for inheritance (base classes)
            if "bases" in cls and cls["bases"]:
                importance_score += 1
                reasons.append("inheritance")
            
            if importance_score >= 2:
                important.append({
                    "name": name,
                    "line_number": cls.get("line_number", 0),
                    "methods_count": methods_count,
                    "importance_score": importance_score,
                    "reasons": reasons,
                    "methods": cls.get("methods", []),
                    "docstring": cls.get("docstring"),
                })
        
        # Sort by importance score
        important.sort(key=lambda x: x["importance_score"], reverse=True)
        
        return important
    
    @staticmethod
    def prioritize_files_for_ai(files_data: List[Dict[str, Any]], max_files: int = 10) -> List[Dict[str, Any]]:
        """
        Prioritize files for AI analysis based on complexity and importance
        
        Args:
            files_data: List of file analysis data
            max_files: Maximum number of files to return
            
        Returns:
            Prioritized list of files
        """
        prioritized = []
        
        for file_data in files_data:
            priority_score = 0
            reasons = []
            
            # Check file structure
            structure = file_data.get("structure", {})
            classes_count = len(structure.get("classes", []))
            functions_count = len(structure.get("functions", []))
            
            if classes_count > 0:
                priority_score += classes_count * 2
                reasons.append(f"{classes_count}_classes")
            
            if functions_count > 0:
                priority_score += functions_count
                reasons.append(f"{functions_count}_functions")
            
            # Check metrics
            metrics = file_data.get("metrics", {})
            complexity = metrics.get("complexity", [])
            
            if complexity:
                avg_complexity = sum(c.get("complexity", 0) for c in complexity) / len(complexity)
                if avg_complexity > 10:
                    priority_score += 5
                    reasons.append("high_complexity")
                elif avg_complexity > 5:
                    priority_score += 3
                    reasons.append("moderate_complexity")
            
            # Check maintainability index
            mi = metrics.get("maintainability_index")
            if mi and mi < 50:
                priority_score += 3
                reasons.append("low_maintainability")
            
            # Avoid test files (lower priority)
            file_path = file_data.get("file_path", "")
            if "test" in file_path.lower():
                priority_score = priority_score // 2
                reasons.append("test_file")
            
            prioritized.append({
                "file_path": file_path,
                "priority_score": priority_score,
                "reasons": reasons,
                "classes_count": classes_count,
                "functions_count": functions_count,
                "data": file_data,
            })
        
        # Sort by priority score
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return prioritized[:max_files]
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Estimate the number of tokens in text (rough approximation)
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        # Rough estimation: ~4 characters per token on average
        # This is a simplification; actual tokenization varies by model
        return len(text) // 4
    
    @staticmethod
    def truncate_code_for_context(code: str, max_tokens: int = 2000) -> Tuple[str, bool]:
        """
        Truncate code to fit within token limit while preserving structure
        
        Args:
            code: Code to truncate
            max_tokens: Maximum tokens allowed
            
        Returns:
            Tuple of (truncated_code, was_truncated)
        """
        estimated_tokens = AIHelpers.estimate_tokens(code)
        
        if estimated_tokens <= max_tokens:
            return code, False
        
        # Calculate how much to keep (with some buffer)
        max_chars = max_tokens * 4 * 0.9  # 90% to be safe
        
        if len(code) <= max_chars:
            return code, False
        
        # Try to truncate at a logical boundary (end of function/class)
        lines = code.split('\n')
        truncated_lines = []
        current_length = 0
        
        for line in lines:
            if current_length + len(line) > max_chars:
                break
            truncated_lines.append(line)
            current_length += len(line) + 1  # +1 for newline
        
        truncated_code = '\n'.join(truncated_lines)
        truncated_code += "\n\n# ... (code truncated for context length)"
        
        return truncated_code, True
    
    @staticmethod
    def extract_code_summary_info(code: str, language: str) -> Dict[str, Any]:
        """
        Extract basic summary information from code
        
        Args:
            code: Code content
            language: Programming language
            
        Returns:
            Dictionary with summary information
        """
        lines = code.split('\n')
        
        info = {
            "total_lines": len(lines),
            "non_empty_lines": len([l for l in lines if l.strip()]),
            "comment_lines": 0,
            "has_classes": False,
            "has_functions": False,
            "has_imports": False,
            "estimated_tokens": AIHelpers.estimate_tokens(code),
        }
        
        # Language-specific patterns
        if language == "python":
            info["comment_lines"] = len([l for l in lines if l.strip().startswith('#')])
            info["has_classes"] = 'class ' in code
            info["has_functions"] = 'def ' in code
            info["has_imports"] = 'import ' in code or 'from ' in code
            
        elif language in ["javascript", "typescript"]:
            info["comment_lines"] = len([l for l in lines if l.strip().startswith('//')])
            info["has_classes"] = 'class ' in code
            info["has_functions"] = 'function ' in code or '=>' in code
            info["has_imports"] = 'import ' in code or 'require(' in code
            
        elif language == "java":
            info["comment_lines"] = len([l for l in lines if l.strip().startswith('//')])
            info["has_classes"] = 'class ' in code
            info["has_functions"] = True  # Java always has methods
            info["has_imports"] = 'import ' in code
        
        return info


# Made with Bob