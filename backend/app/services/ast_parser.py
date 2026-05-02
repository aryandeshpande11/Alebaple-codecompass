"""
AST parser service for extracting code components from Python files.
"""

import ast
from pathlib import Path
from typing import Any


class ASTParser:
    """Service for parsing Python code using AST."""
    
    def __init__(self):
        """Initialize the AST parser."""
        pass
    
    def parse_file(self, file_path: Path) -> dict[str, Any]:
        """
        Parse a Python file and extract code components.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary containing extracted code components
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code, filename=str(file_path))
            
            return {
                "file_path": str(file_path),
                "classes": self._extract_classes(tree),
                "functions": self._extract_functions(tree),
                "imports": self._extract_imports(tree),
                "constants": self._extract_constants(tree),
                "docstring": ast.get_docstring(tree),
            }
        except SyntaxError as e:
            return {
                "file_path": str(file_path),
                "error": f"Syntax error: {str(e)}",
                "classes": [],
                "functions": [],
                "imports": [],
                "constants": [],
                "docstring": None,
            }
        except Exception as e:
            return {
                "file_path": str(file_path),
                "error": f"Parse error: {str(e)}",
                "classes": [],
                "functions": [],
                "imports": [],
                "constants": [],
                "docstring": None,
            }
    
    def _extract_classes(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Extract class definitions from AST."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line_number": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                    "bases": [self._get_name(base) for base in node.bases],
                    "decorators": [self._get_name(dec) for dec in node.decorator_list],
                })
        return classes
    
    def _extract_functions(self, tree: ast.Module) -> list[dict[str, Any]]:
        """Extract function definitions from AST (module-level only)."""
        functions = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "line_number": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "args": [arg.arg for arg in node.args.args],
                    "returns": self._get_name(node.returns) if node.returns else None,
                    "decorators": [self._get_name(dec) for dec in node.decorator_list],
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                })
        return functions
    
    def _extract_imports(self, tree: ast.AST) -> list[dict[str, Any]]:
        """Extract import statements from AST."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "type": "import",
                        "module": alias.name,
                        "alias": alias.asname,
                        "line_number": node.lineno,
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append({
                        "type": "from_import",
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "line_number": node.lineno,
                    })
        return imports
    
    def _extract_constants(self, tree: ast.Module) -> list[dict[str, Any]]:
        """Extract module-level constants from AST."""
        constants = []
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        constants.append({
                            "name": target.id,
                            "line_number": node.lineno,
                            "value": self._get_constant_value(node.value),
                        })
        return constants
    
    def _get_name(self, node: ast.AST | None) -> str:
        """Get the name from an AST node."""
        if node is None:
            return ""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_name(node.slice)}]"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return ast.unparse(node) if hasattr(ast, 'unparse') else ""
    
    def _get_constant_value(self, node: ast.AST) -> Any:
        """Get the value of a constant node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return f"<{node.__class__.__name__.lower()}>"
        elif isinstance(node, ast.Dict):
            return "<dict>"
        return "<complex>"
    
    def get_file_summary(self, file_path: Path) -> dict[str, Any]:
        """
        Get a summary of a Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary containing file summary
        """
        parsed = self.parse_file(file_path)
        
        return {
            "file_path": parsed["file_path"],
            "has_error": "error" in parsed,
            "num_classes": len(parsed.get("classes", [])),
            "num_functions": len(parsed.get("functions", [])),
            "num_imports": len(parsed.get("imports", [])),
            "num_constants": len(parsed.get("constants", [])),
            "has_docstring": parsed.get("docstring") is not None,
        }

# Made with Bob
