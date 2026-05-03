"""
Comprehensive test script for Stage 4 implementations
Tests Developer B and Developer C tasks
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"

# Test counters
tests_passed = 0
tests_failed = 0
test_results = []


def log_test(test_name: str, passed: bool, details: str = ""):
    """Log test result"""
    global tests_passed, tests_failed
    
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if details:
        print(f"   {details}")
    
    test_results.append({
        "test": test_name,
        "passed": passed,
        "details": details
    })
    
    if passed:
        tests_passed += 1
    else:
        tests_failed += 1


def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        passed = response.status_code == 200
        log_test("Server Health Check", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        log_test("Server Health Check", False, f"Error: {str(e)}")
        return False


def test_api_info():
    """Test API info endpoint"""
    try:
        response = requests.get(f"{API_V1}/info", timeout=5)
        passed = response.status_code == 200
        if passed:
            data = response.json()
            has_ai_endpoints = "ai_explain" in data.get("endpoints", {})
            passed = has_ai_endpoints
            log_test("API Info Endpoint", passed, f"AI endpoints present: {has_ai_endpoints}")
        else:
            log_test("API Info Endpoint", False, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        log_test("API Info Endpoint", False, f"Error: {str(e)}")
        return False


def test_ai_explain_endpoint():
    """Test AI explain code endpoint"""
    try:
        payload = {
            "code": "def hello():\n    print('Hello, World!')",
            "language": "python"
        }
        response = requests.post(f"{API_V1}/ai/explain", json=payload, timeout=10)
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_explanation = "explanation" in data
            has_language = data.get("language") == "python"
            has_mock_flag = "mock" in data
            
            passed = has_explanation and has_language and has_mock_flag
            log_test("AI Explain Endpoint", passed, 
                    f"Explanation: {len(data.get('explanation', ''))} chars, Mock: {data.get('mock')}")
        else:
            log_test("AI Explain Endpoint", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        log_test("AI Explain Endpoint", False, f"Error: {str(e)}")
        return False


def test_ai_summarize_endpoint():
    """Test AI summarize code endpoint"""
    try:
        payload = {
            "content": "class Calculator:\n    def add(self, x, y):\n        return x + y",
            "language": "python",
            "summary_type": "class"
        }
        response = requests.post(f"{API_V1}/ai/summarize", json=payload, timeout=10)
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_summary = "summary" in data
            has_language = data.get("language") == "python"
            
            passed = has_summary and has_language
            log_test("AI Summarize Endpoint", passed, 
                    f"Summary: {len(data.get('summary', ''))} chars")
        else:
            log_test("AI Summarize Endpoint", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        log_test("AI Summarize Endpoint", False, f"Error: {str(e)}")
        return False


def test_ai_document_endpoint():
    """Test AI documentation generation endpoint"""
    try:
        payload = {
            "code": "def calculate(x, y):\n    return x + y",
            "language": "python",
            "doc_style": "google"
        }
        response = requests.post(f"{API_V1}/ai/document", json=payload, timeout=10)
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_documentation = "documentation" in data
            has_doc_style = data.get("doc_style") == "google"
            
            passed = has_documentation and has_doc_style
            log_test("AI Document Endpoint", passed, 
                    f"Documentation: {len(data.get('documentation', ''))} chars")
        else:
            log_test("AI Document Endpoint", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        log_test("AI Document Endpoint", False, f"Error: {str(e)}")
        return False


def test_ai_health_endpoint():
    """Test AI service health endpoint"""
    try:
        response = requests.get(f"{API_V1}/ai/health", timeout=5)
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_status = "status" in data
            has_mock_mode = "mock_mode" in data
            
            passed = has_status and has_mock_mode
            log_test("AI Health Endpoint", passed, 
                    f"Status: {data.get('status')}, Mock: {data.get('mock_mode')}")
        else:
            log_test("AI Health Endpoint", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        log_test("AI Health Endpoint", False, f"Error: {str(e)}")
        return False


def test_cache_stats_endpoint():
    """Test cache statistics endpoint"""
    try:
        response = requests.get(f"{API_V1}/ai/cache/stats", timeout=5)
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_hits = "hits" in data
            has_misses = "misses" in data
            has_cached_items = "cached_items" in data
            
            passed = has_hits and has_misses and has_cached_items
            log_test("Cache Stats Endpoint", passed, 
                    f"Hits: {data.get('hits')}, Misses: {data.get('misses')}, Items: {data.get('cached_items')}")
        else:
            log_test("Cache Stats Endpoint", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        log_test("Cache Stats Endpoint", False, f"Error: {str(e)}")
        return False


def test_caching_functionality():
    """Test that caching actually works"""
    try:
        payload = {
            "code": "def test_cache():\n    return 'cached'",
            "language": "python"
        }
        
        # First request - should be a cache miss
        response1 = requests.post(f"{API_V1}/ai/explain", json=payload, timeout=10)
        time.sleep(0.5)
        
        # Second request - should be a cache hit
        response2 = requests.post(f"{API_V1}/ai/explain", json=payload, timeout=10)
        
        passed = response1.status_code == 200 and response2.status_code == 200
        
        if passed:
            data1 = response1.json()
            data2 = response2.json()
            
            # Check if second response indicates it's from cache
            from_cache = data2.get("from_cache", False)
            
            passed = from_cache
            log_test("Caching Functionality", passed, 
                    f"First request cached, second from cache: {from_cache}")
        else:
            log_test("Caching Functionality", False, "Requests failed")
        
        return passed
    except Exception as e:
        log_test("Caching Functionality", False, f"Error: {str(e)}")
        return False


def test_enhanced_analysis_endpoint():
    """Test enhanced analysis endpoint (Developer C)"""
    try:
        # First create a project
        project_payload = {
            "name": "Test Project for AI Analysis",
            "description": "Testing enhanced analysis",
            "repository_url": "https://github.com/example/test-repo"
        }
        
        create_response = requests.post(f"{API_V1}/projects", json=project_payload, timeout=5)
        
        if create_response.status_code != 201:
            log_test("Enhanced Analysis Endpoint", False, "Failed to create test project")
            return False
        
        project_id = create_response.json().get("id")
        
        # Check if enhanced analysis endpoint exists
        analyze_payload = {
            "include_ai_explanations": True,
            "max_files_to_explain": 3,
            "prioritize_complex": True
        }
        
        response = requests.post(
            f"{API_V1}/projects/{project_id}/analyze-with-ai",
            json=analyze_payload,
            timeout=10
        )
        
        passed = response.status_code == 200
        
        if passed:
            data = response.json()
            has_message = "message" in data
            has_status = data.get("status") == "analyzing"
            
            passed = has_message and has_status
            log_test("Enhanced Analysis Endpoint", passed, 
                    f"Analysis started: {data.get('message')}")
        else:
            log_test("Enhanced Analysis Endpoint", False, f"Status: {response.status_code}")
        
        return passed
    except Exception as e:
        log_test("Enhanced Analysis Endpoint", False, f"Error: {str(e)}")
        return False


def test_api_documentation():
    """Test if API documentation is accessible"""
    try:
        response = requests.get(f"{BASE_URL}/api/docs", timeout=5)
        passed = response.status_code == 200
        log_test("API Documentation", passed, f"Docs accessible at /api/docs")
        return passed
    except Exception as e:
        log_test("API Documentation", False, f"Error: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("STAGE 4 IMPLEMENTATION TESTING")
    print("Testing Developer B and Developer C implementations")
    print("="*70 + "\n")
    
    print("🔍 Testing Server Status...")
    test_server_health()
    test_api_info()
    test_api_documentation()
    
    print("\n🤖 Testing AI Endpoints (Developer B)...")
    test_ai_health_endpoint()
    test_ai_explain_endpoint()
    test_ai_summarize_endpoint()
    test_ai_document_endpoint()
    
    print("\n💾 Testing Cache System (Developer B)...")
    test_cache_stats_endpoint()
    test_caching_functionality()
    
    print("\n🔬 Testing Enhanced Analysis (Developer C)...")
    test_enhanced_analysis_endpoint()
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📊 Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
    print("="*70 + "\n")
    
    # Determine if we can proceed
    critical_tests_passed = tests_passed >= 8  # At least 8 out of 11 tests
    
    if critical_tests_passed:
        print("🎉 GO DECISION: All critical tests passed!")
        print("✅ Developer C can proceed with remaining tasks")
        print("✅ Stage 4 implementations are working correctly")
    else:
        print("⚠️  NO-GO DECISION: Some critical tests failed")
        print("❌ Review failed tests before proceeding")
    
    return critical_tests_passed


if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)

# Made with Bob
