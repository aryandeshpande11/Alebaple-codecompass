"""
IBM watsonx.ai Service
Core AI service for code explanation, summarization, and documentation generation
"""

import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from app.core.ai_config import get_ai_config
from app.services.prompt_templates import PromptTemplates

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    """
    Service for interacting with IBM watsonx.ai
    Provides code explanation, summarization, and documentation generation
    """
    
    def __init__(self):
        """Initialize the AI service"""
        self.config = get_ai_config()
        self.prompt_templates = PromptTemplates()
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the watsonx.ai client"""
        if self.config.use_mock_responses:
            logger.info("AI Service initialized in MOCK mode")
            self._client = None
            return
        
        if not self.config.is_configured():
            logger.warning("watsonx.ai credentials not configured. Using mock responses.")
            self.config.use_mock_responses = True
            return
        
        try:
            # Import watsonx.ai SDK (only when not in mock mode)
            from ibm_watsonx_ai import APIClient
            from ibm_watsonx_ai import Credentials
            
            credentials = Credentials(
                url=self.config.watsonx_url,
                api_key=self.config.watsonx_api_key,
            )
            
            self._client = APIClient(credentials)
            self._client.set.default_project(self.config.watsonx_project_id)
            
            logger.info("watsonx.ai client initialized successfully")
            
        except ImportError:
            logger.warning("ibm-watsonx-ai package not installed. Using mock responses.")
            self.config.use_mock_responses = True
            self._client = None
        except Exception as e:
            logger.error(f"Failed to initialize watsonx.ai client: {e}")
            logger.warning("Falling back to mock responses")
            self.config.use_mock_responses = True
            self._client = None
    
    def explain_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Explain a code snippet
        
        Args:
            code: The code snippet to explain
            language: Programming language (python, java, javascript, typescript)
            
        Returns:
            Dictionary containing explanation and metadata
        """
        start_time = time.time()
        
        try:
            prompt = self.prompt_templates.get_code_explanation_prompt(code, language)
            
            if self.config.use_mock_responses:
                response_text = self._generate_mock_explanation(code, language)
            else:
                response_text = self._call_watsonx_api(prompt)
            
            duration = time.time() - start_time
            
            return {
                "explanation": response_text,
                "language": language,
                "code_length": len(code),
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": round(duration, 2),
                "model": self.config.watsonx_model_id,
                "mock": self.config.use_mock_responses,
            }
            
        except Exception as e:
            logger.error(f"Error explaining code: {e}")
            return {
                "error": str(e),
                "language": language,
                "timestamp": datetime.utcnow().isoformat(),
            }
    
    def summarize_file(self, file_content: str, language: str, file_path: str = "") -> Dict[str, Any]:
        """
        Summarize an entire file
        
        Args:
            file_content: Complete file content
            language: Programming language
            file_path: Optional file path for context
            
        Returns:
            Dictionary containing summary and metadata
        """
        start_time = time.time()
        
        try:
            prompt = self.prompt_templates.get_file_summary_prompt(
                file_content, language, file_path
            )
            
            if self.config.use_mock_responses:
                response_text = self._generate_mock_summary(file_content, language, file_path)
            else:
                response_text = self._call_watsonx_api(prompt)
            
            duration = time.time() - start_time
            
            return {
                "summary": response_text,
                "language": language,
                "file_path": file_path,
                "file_size": len(file_content),
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": round(duration, 2),
                "model": self.config.watsonx_model_id,
                "mock": self.config.use_mock_responses,
            }
            
        except Exception as e:
            logger.error(f"Error summarizing file: {e}")
            return {
                "error": str(e),
                "language": language,
                "file_path": file_path,
                "timestamp": datetime.utcnow().isoformat(),
            }
    
    def generate_documentation(self, code: str, language: str) -> Dict[str, Any]:
        """
        Generate documentation for code
        
        Args:
            code: The code to document
            language: Programming language
            
        Returns:
            Dictionary containing documentation and metadata
        """
        start_time = time.time()
        
        try:
            prompt = self.prompt_templates.get_documentation_prompt(code, language)
            
            if self.config.use_mock_responses:
                response_text = self._generate_mock_documentation(code, language)
            else:
                response_text = self._call_watsonx_api(prompt)
            
            duration = time.time() - start_time
            
            return {
                "documentation": response_text,
                "language": language,
                "code_length": len(code),
                "timestamp": datetime.utcnow().isoformat(),
                "duration_seconds": round(duration, 2),
                "model": self.config.watsonx_model_id,
                "mock": self.config.use_mock_responses,
            }
            
        except Exception as e:
            logger.error(f"Error generating documentation: {e}")
            return {
                "error": str(e),
                "language": language,
                "timestamp": datetime.utcnow().isoformat(),
            }
    
    def _call_watsonx_api(self, prompt: str) -> str:
        """
        Call the watsonx.ai API with retry logic
        
        Args:
            prompt: The prompt to send
            
        Returns:
            Generated text response
        """
        if self._client is None:
            raise RuntimeError("watsonx.ai client not initialized")
        
        from ibm_watsonx_ai.foundation_models import ModelInference
        
        model = ModelInference(
            model_id=self.config.watsonx_model_id,
            api_client=self._client,
            params=self.config.get_generation_params(),
        )
        
        for attempt in range(self.config.max_retries):
            try:
                response = model.generate_text(prompt=prompt)
                return response
                
            except Exception as e:
                if attempt < self.config.max_retries - 1:
                    logger.warning(f"API call failed (attempt {attempt + 1}): {e}")
                    time.sleep(self.config.retry_delay * (attempt + 1))
                else:
                    raise
        
        raise RuntimeError("Max retries exceeded")
    
    def _generate_mock_explanation(self, code: str, language: str) -> str:
        """Generate a mock explanation for testing with structured data"""
        lines = code.strip().split('\n')
        num_lines = len(lines)
        
        # Try to detect code patterns
        has_class = any('class ' in line for line in lines)
        has_function = any('def ' in line or 'function ' in line for line in lines)
        has_import = any('import ' in line or 'require(' in line for line in lines)
        has_loop = any(keyword in code for keyword in ['for ', 'while ', 'forEach'])
        has_conditional = any(keyword in code for keyword in ['if ', 'else', 'switch', 'case'])
        
        # Calculate complexity score
        complexity_score = 0
        if has_class: complexity_score += 2
        if has_function: complexity_score += 1
        if has_loop: complexity_score += 2
        if has_conditional: complexity_score += 1
        if num_lines > 50: complexity_score += 2
        if num_lines > 100: complexity_score += 2
        
        complexity_level = 'Low' if complexity_score <= 2 else 'Medium' if complexity_score <= 5 else 'High' if complexity_score <= 8 else 'Very High'
        
        explanation = f"""## 📊 Code Analysis Overview

This {language} code contains **{num_lines} lines** with a complexity rating of **{complexity_level}**.

### 🎯 Purpose & Functionality

"""
        
        if has_class:
            explanation += "- **Object-Oriented Design**: Defines classes with methods and properties for structured data management\n"
        if has_function:
            explanation += "- **Modular Functions**: Contains reusable function definitions that encapsulate specific logic\n"
        if has_import:
            explanation += "- **External Dependencies**: Imports modules/libraries to extend functionality\n"
        if has_loop:
            explanation += "- **Iterative Processing**: Uses loops for data iteration and repetitive operations\n"
        if has_conditional:
            explanation += "- **Conditional Logic**: Implements decision-making with if/else statements\n"
        
        explanation += f"""

### 🔍 Key Components

1. **Language**: {language.title()}
2. **Structure**: {'Object-Oriented' if has_class else 'Procedural/Functional'}
3. **Dependencies**: {'External libraries required' if has_import else 'Self-contained with built-in features'}
4. **Lines of Code**: {num_lines}

### 📈 Complexity Metrics

- **Complexity Level**: {complexity_level}
- **Complexity Score**: {complexity_score}/10
- **Maintainability**: {'Excellent' if complexity_score <= 3 else 'Good' if complexity_score <= 6 else 'Moderate' if complexity_score <= 8 else 'Needs Improvement'}

**Breakdown**:
- Classes: {'Yes ✓' if has_class else 'No ✗'}
- Functions: {'Yes ✓' if has_function else 'No ✗'}
- Loops: {'Yes ✓' if has_loop else 'No ✗'}
- Conditionals: {'Yes ✓' if has_conditional else 'No ✗'}

### 🔄 Logic Flow

The code follows a {'top-down' if not has_class else 'object-oriented'} execution pattern:

1. {'Import statements load required dependencies' if has_import else 'Uses built-in language features'}
2. {'Class definitions establish data structures and behaviors' if has_class else 'Function definitions create reusable logic blocks'}
3. {'Methods process data and implement business logic' if has_class else 'Functions execute specific operations'}
4. {'Control flow manages execution paths' if has_conditional or has_loop else 'Linear execution from top to bottom'}

### ✅ Best Practices Observed

- ✓ Follows {language} naming conventions
- ✓ {'Proper use of OOP principles' if has_class else 'Clear functional decomposition'}
- ✓ {'Modular design with separated concerns' if has_function else 'Straightforward implementation'}

### ⚠️ Recommendations

1. **Documentation**: Add comprehensive docstrings/comments for complex logic
2. **Error Handling**: Implement try-catch blocks for robust error management
3. **Testing**: Create unit tests to verify functionality
4. **Performance**: {'Consider optimization for large datasets' if has_loop else 'Review for potential bottlenecks'}
5. **Security**: Validate all inputs and sanitize user data

### 📚 Dependencies Analysis

{'**External Modules**: This code relies on external libraries. Ensure all dependencies are properly installed and version-controlled.' if has_import else '**Self-Contained**: No external dependencies detected. Code uses only built-in language features.'}

---
*🤖 AI-Generated Analysis | Complexity Score: {complexity_score}/10 | Confidence: High*
"""
        
        return explanation
    
    def _generate_mock_summary(self, file_content: str, language: str, file_path: str) -> str:
        """Generate a mock file summary for testing"""
        lines = file_content.strip().split('\n')
        num_lines = len(lines)
        
        file_name = file_path.split('/')[-1] if file_path else "this file"
        
        summary = f"""**Purpose**
{file_name} is a {language} source file containing {num_lines} lines of code. It serves as a module within the larger application, providing specific functionality and components.

**Key Exports**
- Multiple functions and/or classes that can be imported by other modules
- Utility functions for common operations
- Data structures and type definitions

**Dependencies**
This file imports several external modules and may depend on other project files. Dependencies include both standard library modules and third-party packages.

**Complexity Level**
Medium - The file contains a moderate amount of logic with clear structure and organization. It balances functionality with maintainability.

**Role in Project**
This file likely serves as a core component in the application architecture. It may be imported by other modules and provides essential functionality for the project's operation.

*Note: This is a mock AI response for development/testing purposes.*"""
        
        return summary
    
    def _generate_mock_documentation(self, code: str, language: str) -> str:
        """Generate mock documentation for testing"""
        doc_style = {
            "python": "Google-style docstrings",
            "java": "JavaDoc",
            "javascript": "JSDoc",
            "typescript": "TSDoc",
        }.get(language.lower(), "standard documentation")
        
        documentation = f"""**Module/Function Description**
This code component provides specific functionality within the {language} application. It is designed to be reusable and maintainable.

**Parameters**
- param1 (type): Description of the first parameter
- param2 (type): Description of the second parameter
- options (optional): Additional configuration options

**Return Values**
Returns a value of appropriate type based on the operation performed. Returns null/None in case of errors.

**Exceptions/Errors**
- ValueError: Raised when invalid input is provided
- RuntimeError: Raised when operation cannot be completed
- TypeError: Raised when incorrect types are passed

**Usage Examples**

Example 1: Basic usage
```{language}
// Initialize and use the component
result = component.method(param1, param2)
```

Example 2: With options
```{language}
// Use with additional configuration
result = component.method(param1, param2, {{option: value}})
```

**Notes**
- This documentation follows {doc_style} conventions
- Ensure proper error handling when using this component
- Consider performance implications for large-scale operations
- Thread-safety considerations may apply in concurrent environments

*Note: This is a mock AI response for development/testing purposes.*"""
        
        return documentation
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health status of the AI service
        
        Returns:
            Dictionary with health status information
        """
        return {
            "status": "healthy",
            "mock_mode": self.config.use_mock_responses,
            "configured": self.config.is_configured(),
            "model": self.config.watsonx_model_id,
            "timestamp": datetime.utcnow().isoformat(),
        }


# Global service instance
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """Get or create the global AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service


def reload_ai_service() -> AIService:
    """Force reload the AI service instance (useful after config changes)"""
    global _ai_service
    _ai_service = AIService()
    return _ai_service


# Made with Bob