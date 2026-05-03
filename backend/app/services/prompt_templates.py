"""
Prompt Templates for IBM watsonx.ai Code Analysis
Language-specific prompts for code explanation, documentation, and summarization
"""

from typing import Dict, Any


class PromptTemplates:
    """Manages prompt templates for different AI operations and languages"""
    
    # Language-specific context
    LANGUAGE_CONTEXT = {
        "python": "Python is a high-level, interpreted programming language known for its readability and versatility.",
        "java": "Java is a class-based, object-oriented programming language designed for platform independence.",
        "javascript": "JavaScript is a high-level, interpreted scripting language primarily used for web development.",
        "typescript": "TypeScript is a strongly typed superset of JavaScript that compiles to plain JavaScript.",
    }
    
    @staticmethod
    def get_code_explanation_prompt(code: str, language: str) -> str:
        """
        Generate a prompt for explaining code
        
        Args:
            code: The code snippet to explain
            language: Programming language (python, java, javascript, typescript)
            
        Returns:
            Formatted prompt string
        """
        context = PromptTemplates.LANGUAGE_CONTEXT.get(
            language.lower(), 
            f"{language} is a programming language."
        )
        
        return f"""You are an expert software engineer analyzing {language} code.

Context: {context}

Please analyze the following {language} code and provide a comprehensive explanation:

```{language}
{code}
```

Provide your analysis in the following format:

1. **Overview**: Brief summary of what this code does (2-3 sentences)

2. **Key Components**: List and explain the main components (functions, classes, variables)

3. **Logic Flow**: Explain the execution flow and any important algorithms

4. **Dependencies**: Identify external libraries or modules used

5. **Complexity**: Assess the code complexity (simple, moderate, complex) and explain why

6. **Best Practices**: Note any good practices or potential improvements

7. **Potential Issues**: Identify any bugs, security concerns, or performance issues

Keep your explanation clear, concise, and suitable for developers who are new to this codebase."""
    
    @staticmethod
    def get_file_summary_prompt(file_content: str, language: str, file_path: str = "") -> str:
        """
        Generate a prompt for summarizing an entire file
        
        Args:
            file_content: Complete file content
            language: Programming language
            file_path: Optional file path for context
            
        Returns:
            Formatted prompt string
        """
        path_context = f" (from {file_path})" if file_path else ""
        
        return f"""You are an expert software engineer reviewing a {language} file{path_context}.

Please provide a concise summary of this file:

```{language}
{file_content}
```

Provide your summary in the following format:

1. **Purpose**: What is the main purpose of this file? (1-2 sentences)

2. **Key Exports**: List the main classes, functions, or components exported

3. **Dependencies**: What external modules or libraries does it use?

4. **Complexity Level**: Rate as Low, Medium, or High and explain briefly

5. **Role in Project**: How might this file fit into a larger application?

Keep the summary concise but informative, suitable for quick onboarding."""
    
    @staticmethod
    def get_documentation_prompt(code: str, language: str) -> str:
        """
        Generate a prompt for creating documentation
        
        Args:
            code: The code to document
            language: Programming language
            
        Returns:
            Formatted prompt string
        """
        doc_style = {
            "python": "Google-style docstrings",
            "java": "JavaDoc format",
            "javascript": "JSDoc format",
            "typescript": "TSDoc format",
        }.get(language.lower(), "standard documentation format")
        
        return f"""You are a technical writer creating documentation for {language} code.

Generate comprehensive documentation for the following code using {doc_style}:

```{language}
{code}
```

Provide documentation that includes:

1. **Module/Class/Function Description**: Clear explanation of purpose

2. **Parameters**: Document all parameters with types and descriptions

3. **Return Values**: Describe what is returned and when

4. **Exceptions/Errors**: List possible exceptions or error conditions

5. **Usage Examples**: Provide 1-2 practical usage examples

6. **Notes**: Any important implementation details or caveats

Format the documentation according to {doc_style} conventions."""
    
    @staticmethod
    def get_class_summary_prompt(class_code: str, language: str, class_name: str) -> str:
        """
        Generate a prompt for summarizing a class
        
        Args:
            class_code: The class code
            language: Programming language
            class_name: Name of the class
            
        Returns:
            Formatted prompt string
        """
        return f"""You are analyzing a {language} class named '{class_name}'.

```{language}
{class_code}
```

Provide a structured summary:

1. **Class Purpose**: What is this class responsible for?

2. **Key Methods**: List and briefly describe the main public methods

3. **Properties/Fields**: Important instance variables or properties

4. **Design Pattern**: Does it follow any recognizable design patterns?

5. **Usage Context**: When and how would this class be used?

6. **Relationships**: Does it extend/implement other classes or interfaces?

Keep it concise and focused on helping developers understand the class quickly."""
    
    @staticmethod
    def get_function_summary_prompt(function_code: str, language: str, function_name: str) -> str:
        """
        Generate a prompt for summarizing a function
        
        Args:
            function_code: The function code
            language: Programming language
            function_name: Name of the function
            
        Returns:
            Formatted prompt string
        """
        return f"""You are analyzing a {language} function named '{function_name}'.

```{language}
{function_code}
```

Provide a concise summary:

1. **Purpose**: What does this function do? (1 sentence)

2. **Input**: What parameters does it accept?

3. **Output**: What does it return?

4. **Side Effects**: Does it modify state or have side effects?

5. **Complexity**: Time/space complexity if applicable

6. **Usage**: When should this function be called?

Be brief but informative."""
    
    @staticmethod
    def get_batch_analysis_prompt(files_info: list[Dict[str, Any]], language: str) -> str:
        """
        Generate a prompt for analyzing multiple files together
        
        Args:
            files_info: List of file information dictionaries
            language: Primary programming language
            
        Returns:
            Formatted prompt string
        """
        files_list = "\n".join([
            f"- {info.get('path', 'unknown')}: {info.get('description', 'No description')}"
            for info in files_info
        ])
        
        return f"""You are analyzing a {language} project with multiple files.

Files in this analysis:
{files_list}

Provide a project-level analysis:

1. **Project Structure**: How are these files organized?

2. **Architecture**: What architectural patterns are evident?

3. **Dependencies**: How do these files relate to each other?

4. **Entry Points**: Which files are likely entry points?

5. **Key Components**: What are the most important components?

6. **Recommendations**: Suggestions for new developers approaching this code

Focus on the big picture and relationships between components."""


# Made with Bob