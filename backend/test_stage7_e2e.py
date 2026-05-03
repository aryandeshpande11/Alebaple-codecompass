"""
Stage 7: End-to-End Testing Script
Tests all major functionality of the Code Understanding & Onboarding Accelerator
"""

import requests
import json
import time
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, status, message=""):
    """Print test result with color"""
    if status == "PASS":
        print(f"{Colors.GREEN}[PASS] {name}{Colors.END}")
    elif status == "FAIL":
        print(f"{Colors.RED}[FAIL] {name}: {message}{Colors.END}")
    elif status == "SKIP":
        print(f"{Colors.YELLOW}[SKIP] {name}: {message}{Colors.END}")
    else:
        print(f"{Colors.BLUE}[INFO] {name}{Colors.END}")

def test_health_check():
    """Test 1: Health Check"""
    print_test("Health Check", "INFO")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print_test("Backend is running", "PASS")
            return True
        else:
            print_test("Backend health check", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Backend connection", "FAIL", str(e))
        return False

def test_create_project():
    """Test 2: Create Project"""
    print_test("Create Project", "INFO")
    try:
        payload = {
            "name": "Test Project E2E",
            "description": "End-to-end test project"
        }
        response = requests.post(f"{API_BASE}/projects/", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            project_id = data.get("id")
            print_test(f"Project created with ID: {project_id}", "PASS")
            return project_id
        else:
            print_test("Create project", "FAIL", f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Create project", "FAIL", str(e))
        return None

def test_upload_code(project_id):
    """Test 3: Upload Code Files"""
    print_test("Upload Code Files", "INFO")
    try:
        # Create a sample Python file
        sample_code = '''
def calculate_fibonacci(n):
    """Calculate fibonacci number at position n"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

class DataProcessor:
    """Process and analyze data"""
    def __init__(self, data):
        self.data = data
    
    def process(self):
        """Process the data"""
        return [x * 2 for x in self.data]
'''
        
        files = {
            'files': ('test_module.py', sample_code, 'text/plain')
        }
        
        response = requests.post(
            f"{API_BASE}/projects/{project_id}/upload",
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test(f"Uploaded {data.get('files_uploaded', 0)} files", "PASS")
            return True
        else:
            print_test("Upload files", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Upload files", "FAIL", str(e))
        return False

def test_analyze_project(project_id):
    """Test 4: Analyze Project"""
    print_test("Analyze Project", "INFO")
    try:
        response = requests.post(
            f"{API_BASE}/analysis/{project_id}/analyze",
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test(f"Analysis complete - {data.get('total_files', 0)} files analyzed", "PASS")
            return data
        else:
            print_test("Analyze project", "FAIL", f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Analyze project", "FAIL", str(e))
        return None

def test_get_analysis(project_id):
    """Test 5: Get Analysis Results"""
    print_test("Get Analysis Results", "INFO")
    try:
        response = requests.get(
            f"{API_BASE}/analysis/{project_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            metrics = data.get('metrics', {})
            print_test(f"Retrieved analysis - LOC: {metrics.get('total_lines', 0)}", "PASS")
            return data
        else:
            print_test("Get analysis", "FAIL", f"Status: {response.status_code}")
            return None
    except Exception as e:
        print_test("Get analysis", "FAIL", str(e))
        return None

def test_ai_explanation(project_id):
    """Test 6: AI Code Explanation"""
    print_test("AI Code Explanation", "INFO")
    try:
        payload = {
            "code": "def hello(): return 'world'",
            "language": "python",
            "context": "Simple function"
        }
        
        response = requests.post(
            f"{API_BASE}/ai/explain",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            explanation = data.get('explanation', '')
            if len(explanation) > 50:
                print_test(f"AI explanation generated ({len(explanation)} chars)", "PASS")
                return True
            else:
                print_test("AI explanation", "FAIL", "Explanation too short")
                return False
        else:
            print_test("AI explanation", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("AI explanation", "FAIL", str(e))
        return False

def test_file_content(project_id):
    """Test 7: Get File Content"""
    print_test("Get File Content", "INFO")
    try:
        # First get the file list
        response = requests.get(f"{API_BASE}/analysis/{project_id}", timeout=10)
        if response.status_code != 200:
            print_test("Get file list", "FAIL", "Cannot get analysis")
            return False
        
        data = response.json()
        files = data.get('files', [])
        
        if not files:
            print_test("Get file content", "SKIP", "No files to test")
            return True
        
        # Get content of first file
        file_path = files[0].get('path', '')
        response = requests.get(
            f"{API_BASE}/projects/{project_id}/files/{file_path}",
            timeout=10
        )
        
        if response.status_code == 200:
            content = response.json().get('content', '')
            print_test(f"Retrieved file content ({len(content)} chars)", "PASS")
            return True
        else:
            print_test("Get file content", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Get file content", "FAIL", str(e))
        return False

def test_project_list():
    """Test 8: List Projects"""
    print_test("List Projects", "INFO")
    try:
        response = requests.get(f"{API_BASE}/projects/", timeout=10)
        
        if response.status_code == 200:
            projects = response.json()
            print_test(f"Retrieved {len(projects)} projects", "PASS")
            return True
        else:
            print_test("List projects", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("List projects", "FAIL", str(e))
        return False

def test_error_handling():
    """Test 9: Error Handling"""
    print_test("Error Handling", "INFO")
    
    tests_passed = 0
    tests_total = 3
    
    # Test 1: Invalid project ID
    try:
        response = requests.get(f"{API_BASE}/projects/invalid-id-12345", timeout=5)
        if response.status_code == 404:
            print_test("  Invalid project ID returns 404", "PASS")
            tests_passed += 1
        else:
            print_test("  Invalid project ID", "FAIL", f"Expected 404, got {response.status_code}")
    except Exception as e:
        print_test("  Invalid project ID", "FAIL", str(e))
    
    # Test 2: Missing required fields
    try:
        response = requests.post(f"{API_BASE}/projects/", json={}, timeout=5)
        if response.status_code in [400, 422]:
            print_test("  Missing fields returns 400/422", "PASS")
            tests_passed += 1
        else:
            print_test("  Missing fields", "FAIL", f"Expected 400/422, got {response.status_code}")
    except Exception as e:
        print_test("  Missing fields", "FAIL", str(e))
    
    # Test 3: Invalid endpoint
    try:
        response = requests.get(f"{API_BASE}/invalid-endpoint", timeout=5)
        if response.status_code == 404:
            print_test("  Invalid endpoint returns 404", "PASS")
            tests_passed += 1
        else:
            print_test("  Invalid endpoint", "FAIL", f"Expected 404, got {response.status_code}")
    except Exception as e:
        print_test("  Invalid endpoint", "FAIL", str(e))
    
    if tests_passed == tests_total:
        print_test(f"Error handling ({tests_passed}/{tests_total})", "PASS")
        return True
    else:
        print_test(f"Error handling ({tests_passed}/{tests_total})", "FAIL")
        return False

def run_all_tests():
    """Run all end-to-end tests"""
    print("\n" + "="*60)
    print("  STAGE 7: END-TO-END TESTING")
    print("  Code Understanding & Onboarding Accelerator")
    print("="*60 + "\n")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # Test 1: Health Check
    results["total"] += 1
    if test_health_check():
        results["passed"] += 1
    else:
        results["failed"] += 1
        print(f"\n{Colors.RED}Backend is not running. Please start the backend server.{Colors.END}")
        print(f"Run: cd backend && uvicorn app.main:app --reload\n")
        return results
    
    print()
    
    # Test 2: Create Project
    results["total"] += 1
    project_id = test_create_project()
    if project_id:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print(f"\n{Colors.RED}Cannot continue without project creation{Colors.END}\n")
        return results
    
    print()
    
    # Test 3: Upload Code
    results["total"] += 1
    if test_upload_code(project_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    print()
    
    # Test 4: Analyze Project
    results["total"] += 1
    if test_analyze_project(project_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    print()
    
    # Test 5: Get Analysis
    results["total"] += 1
    if test_get_analysis(project_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    print()
    
    # Test 6: AI Explanation
    results["total"] += 1
    if test_ai_explanation(project_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    print()
    
    # Test 7: File Content
    results["total"] += 1
    if test_file_content(project_id):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    print()
    
    # Test 8: Project List
    results["total"] += 1
    if test_project_list():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    print()
    
    # Test 9: Error Handling
    results["total"] += 1
    if test_error_handling():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Print Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    print(f"Total Tests:  {results['total']}")
    print(f"{Colors.GREEN}Passed:       {results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed:       {results['failed']}{Colors.END}")
    print(f"{Colors.YELLOW}Skipped:      {results['skipped']}{Colors.END}")
    
    success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}🎉 ALL TESTS PASSED! System is ready for demo.{Colors.END}\n")
    else:
        print(f"\n{Colors.YELLOW}⚠️  Some tests failed. Please review and fix issues.{Colors.END}\n")
    
    print("="*60 + "\n")
    
    return results

if __name__ == "__main__":
    try:
        results = run_all_tests()
        exit(0 if results['failed'] == 0 else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user{Colors.END}\n")
        exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Unexpected error: {e}{Colors.END}\n")
        exit(1)

# Made with Bob
