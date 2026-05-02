"""
Universal code parser using Tree-sitter for multi-language support.
Supports: Python, Java, JavaScript, TypeScript
"""

from pathlib import Path
from typing import Any, Optional
import tree_sitter_python as tspython
import tree_sitter_java as tsjava
import tree_sitter_javascript as tsjavascript
import tree_sitter_typescript as tstypescript
from tree_sitter import Language, Parser, Node


class UniversalParser:
    """Universal parser for multiple programming languages using Tree-sitter."""
    
    # Language configurations
    LANGUAGE_MAP = {
        '.py': ('python', tspython),
        '.java': ('java', tsjava),
        '.js': ('javascript', tsjavascript),
        '.jsx': ('javascript', tsjavascript),
        '.ts': ('typescript', tstypescript),
        '.tsx': ('tsx', tstypescript),
    }
    
    def __init__(self):
        """Initialize parsers for all supported languages."""
        self.parsers = {}
        self.languages = {}
        
        # Initialize Python
        self.languages['python'] = Language(tspython.language())
        
        # Initialize Java
        self.languages['java'] = Language(tsjava.language())
        
        # Initialize JavaScript
        self.languages['javascript'] = Language(tsjavascript.language())
        
        # Initialize TypeScript (has separate language functions)
        self.languages['typescript'] = Language(tstypescript.language_typescript())
        self.languages['tsx'] = Language(tstypescript.language_tsx())
        
        # Create parsers for each language
        for lang_name, language in self.languages.items():
            parser = Parser(language)
            self.parsers[lang_name] = parser
    
    def detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension."""
        ext = file_path.suffix.lower()
        if ext in self.LANGUAGE_MAP:
            return self.LANGUAGE_MAP[ext][0]
        return None
    
    def parse_file(self, file_path: Path) -> dict[str, Any]:
        """
        Parse a source code file and extract components.
        
        Args:
            file_path: Path to the source file
            
        Returns:
            Dictionary containing extracted code components
        """
        language = self.detect_language(file_path)
        
        if not language:
            return {
                "file_path": str(file_path),
                "language": "unknown",
                "error": f"Unsupported file type: {file_path.suffix}",
                "classes": [],
                "functions": [],
                "imports": [],
                "constants": [],
            }
        
        try:
            with open(file_path, 'rb') as f:
                source_code = f.read()
            
            parser = self.parsers[language]
            tree = parser.parse(source_code)
            
            return {
                "file_path": str(file_path),
                "language": language,
                "classes": self._extract_classes(tree.root_node, source_code, language),
                "functions": self._extract_functions(tree.root_node, source_code, language),
                "imports": self._extract_imports(tree.root_node, source_code, language),
                "constants": self._extract_constants(tree.root_node, source_code, language),
                "docstring": self._extract_docstring(tree.root_node, source_code, language),
            }
        except Exception as e:
            return {
                "file_path": str(file_path),
                "language": language,
                "error": f"Parse error: {str(e)}",
                "classes": [],
                "functions": [],
                "imports": [],
                "constants": [],
            }
    
    def _extract_classes(self, node: Node, source: bytes, language: str) -> list[dict[str, Any]]:
        """Extract class definitions."""
        classes = []
        
        class_queries = {
            'python': '(class_definition name: (identifier) @class.name)',
            'java': '(class_declaration name: (identifier) @class.name)',
            'javascript': '(class_declaration name: (identifier) @class.name)',
            'typescript': '(class_declaration name: (type_identifier) @class.name)',
            'tsx': '(class_declaration name: (type_identifier) @class.name)',
        }
        
        query_str = class_queries.get(language)
        if not query_str:
            return classes
        
        try:
            query = self.languages[language].query(query_str)
            captures = query.captures(node)
            
            for capture_node, capture_name in captures:
                if 'class.name' in capture_name:
                    class_node = capture_node.parent
                    classes.append({
                        "name": source[capture_node.start_byte:capture_node.end_byte].decode('utf-8'),
                        "line_number": capture_node.start_point[0] + 1,
                        "methods": self._extract_methods(class_node, source, language),
                    })
        except Exception:
            pass
        
        return classes
    
    def _extract_methods(self, class_node: Node, source: bytes, language: str) -> list[str]:
        """Extract method names from a class."""
        methods = []
        
        method_queries = {
            'python': '(function_definition name: (identifier) @method.name)',
            'java': '(method_declaration name: (identifier) @method.name)',
            'javascript': '(method_definition name: (property_identifier) @method.name)',
            'typescript': '(method_definition name: (property_identifier) @method.name)',
            'tsx': '(method_definition name: (property_identifier) @method.name)',
        }
        
        query_str = method_queries.get(language)
        if not query_str:
            return methods
        
        try:
            query = self.languages[language].query(query_str)
            captures = query.captures(class_node)
            
            for capture_node, capture_name in captures:
                if 'method.name' in capture_name:
                    methods.append(source[capture_node.start_byte:capture_node.end_byte].decode('utf-8'))
        except Exception:
            pass
        
        return methods
    
    def _extract_functions(self, node: Node, source: bytes, language: str) -> list[dict[str, Any]]:
        """Extract function definitions (module-level)."""
        functions = []
        
        function_queries = {
            'python': '(function_definition name: (identifier) @func.name)',
            'java': '(method_declaration name: (identifier) @func.name)',
            'javascript': '(function_declaration name: (identifier) @func.name)',
            'typescript': '(function_declaration name: (identifier) @func.name)',
            'tsx': '(function_declaration name: (identifier) @func.name)',
        }
        
        query_str = function_queries.get(language)
        if not query_str:
            return functions
        
        try:
            query = self.languages[language].query(query_str)
            captures = query.captures(node)
            
            for capture_node, capture_name in captures:
                if 'func.name' in capture_name:
                    # Check if it's not inside a class
                    parent = capture_node.parent
                    is_method = False
                    
                    while parent:
                        if parent.type in ['class_definition', 'class_declaration', 'class_body']:
                            is_method = True
                            break
                        parent = parent.parent
                    
                    if not is_method:
                        functions.append({
                            "name": source[capture_node.start_byte:capture_node.end_byte].decode('utf-8'),
                            "line_number": capture_node.start_point[0] + 1,
                        })
        except Exception:
            pass
        
        return functions
    
    def _extract_imports(self, node: Node, source: bytes, language: str) -> list[dict[str, Any]]:
        """Extract import statements."""
        imports = []
        
        import_queries = {
            'python': '(import_statement) @import',
            'java': '(import_declaration) @import',
            'javascript': '(import_statement) @import',
            'typescript': '(import_statement) @import',
            'tsx': '(import_statement) @import',
        }
        
        query_str = import_queries.get(language)
        if not query_str:
            return imports
        
        try:
            query = self.languages[language].query(query_str)
            captures = query.captures(node)
            
            for capture_node, _ in captures:
                import_text = source[capture_node.start_byte:capture_node.end_byte].decode('utf-8')
                imports.append({
                    "statement": import_text.strip(),
                    "line_number": capture_node.start_point[0] + 1,
                })
        except Exception:
            pass
        
        return imports
    
    def _extract_constants(self, node: Node, source: bytes, language: str) -> list[dict[str, Any]]:
        """Extract constants (uppercase variables in Python, final in Java, const in JS/TS)."""
        constants = []
        
        # This is simplified - would need more sophisticated queries for each language
        if language == 'python':
            try:
                query_str = '(assignment left: (identifier) @const.name)'
                query = self.languages[language].query(query_str)
                captures = query.captures(node)
                
                for capture_node, capture_name in captures:
                    if 'const.name' in capture_name:
                        name = source[capture_node.start_byte:capture_node.end_byte].decode('utf-8')
                        if name.isupper():
                            constants.append({
                                "name": name,
                                "line_number": capture_node.start_point[0] + 1,
                            })
            except Exception:
                pass
        
        return constants
    
    def _extract_docstring(self, node: Node, source: bytes, language: str) -> Optional[str]:
        """Extract module-level docstring or comment."""
        if language == 'python':
            try:
                query_str = '(module . (expression_statement (string) @docstring))'
                query = self.languages[language].query(query_str)
                captures = query.captures(node)
                
                if captures:
                    capture_node, _ = captures[0]
                    docstring = source[capture_node.start_byte:capture_node.end_byte].decode('utf-8')
                    return docstring.strip('"\'')
            except Exception:
                pass
        
        return None
    
    def get_file_summary(self, file_path: Path) -> dict[str, Any]:
        """
        Get a summary of a source file.
        
        Args:
            file_path: Path to the source file
            
        Returns:
            Dictionary containing file summary
        """
        parsed = self.parse_file(file_path)
        
        return {
            "file_path": parsed["file_path"],
            "language": parsed.get("language", "unknown"),
            "has_error": "error" in parsed,
            "num_classes": len(parsed.get("classes", [])),
            "num_functions": len(parsed.get("functions", [])),
            "num_imports": len(parsed.get("imports", [])),
            "num_constants": len(parsed.get("constants", [])),
            "has_docstring": parsed.get("docstring") is not None,
        }

# Made with Bob
