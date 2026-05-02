"""
Test script for Tree-sitter universal parser
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.universal_parser import UniversalParser


def test_parser():
    """Test the universal parser with different languages."""
    parser = UniversalParser()
    
    print("Testing Universal Parser with Tree-sitter")
    print("=" * 60)
    
    # Test Python file
    print("\n1. Testing Python file parsing...")
    py_file = Path("app/main.py")
    if py_file.exists():
        result = parser.parse_file(py_file)
        print(f"   Language: {result.get('language')}")
        print(f"   Classes: {len(result.get('classes', []))}")
        print(f"   Functions: {len(result.get('functions', []))}")
        print(f"   Imports: {len(result.get('imports', []))}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
    else:
        print("   File not found")
    
    # Test with a simple Python code snippet
    print("\n2. Creating test files...")
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    # Python test
    py_test = test_dir / "test.py"
    py_test.write_text("""
def hello_world():
    '''Say hello'''
    print("Hello, World!")

class MyClass:
    def method(self):
        pass
""")
    
    result = parser.parse_file(py_test)
    print(f"\n   Python Test:")
    print(f"   - Language: {result.get('language')}")
    print(f"   - Classes: {[c['name'] for c in result.get('classes', [])]}")
    print(f"   - Functions: {[f['name'] for f in result.get('functions', [])]}")
    
    # JavaScript test
    js_test = test_dir / "test.js"
    js_test.write_text("""
function greet(name) {
    return `Hello, ${name}!`;
}

class Person {
    constructor(name) {
        this.name = name;
    }
}
""")
    
    result = parser.parse_file(js_test)
    print(f"\n   JavaScript Test:")
    print(f"   - Language: {result.get('language')}")
    print(f"   - Classes: {[c['name'] for c in result.get('classes', [])]}")
    print(f"   - Functions: {[f['name'] for f in result.get('functions', [])]}")
    
    # Java test
    java_test = test_dir / "Test.java"
    java_test.write_text("""
public class Test {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
    
    public void greet() {
        System.out.println("Hi");
    }
}
""")
    
    result = parser.parse_file(java_test)
    print(f"\n   Java Test:")
    print(f"   - Language: {result.get('language')}")
    print(f"   - Classes: {[c['name'] for c in result.get('classes', [])]}")
    
    # TypeScript test
    ts_test = test_dir / "test.ts"
    ts_test.write_text("""
function add(a: number, b: number): number {
    return a + b;
}

class Calculator {
    multiply(a: number, b: number): number {
        return a * b;
    }
}
""")
    
    result = parser.parse_file(ts_test)
    print(f"\n   TypeScript Test:")
    print(f"   - Language: {result.get('language')}")
    print(f"   - Classes: {[c['name'] for c in result.get('classes', [])]}")
    print(f"   - Functions: {[f['name'] for f in result.get('functions', [])]}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)


if __name__ == "__main__":
    try:
        test_parser()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
