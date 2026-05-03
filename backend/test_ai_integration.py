"""
Test script for Stage 4 AI Integration
Tests all AI endpoints and functionality
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_api_info():
    """Test API info endpoint"""
    print_section("Testing API Info")
    
    response = requests.get(f"{BASE_URL}/api/v1/info")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"API Name: {data['api_name']}")
        print(f"Version: {data['version']}")
        print(f"\nEndpoints:")
        for key, value in data['endpoints'].items():
            print(f"  - {key}: {value}")
        print(f"\nFeatures:")
        for feature in data['features']:
            print(f"  - {feature}")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def test_ai_health():
    """Test AI service health check"""
    print_section("Testing AI Health Check")
    
    response = requests.get(f"{BASE_URL}/api/v1/ai/health")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Mock Mode: {data['mock_mode']}")
        print(f"Configured: {data['configured']}")
        print(f"Model: {data['model']}")
        print(f"✅ AI service is healthy")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def test_code_explanation():
    """Test code explanation endpoint"""
    print_section("Testing Code Explanation")
    
    # Test with Python code
    python_code = """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
"""
    
    payload = {
        "code": python_code,
        "language": "python"
    }
    
    print("Sending Python code for explanation...")
    response = requests.post(f"{BASE_URL}/api/v1/ai/explain", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nLanguage: {data['language']}")
        print(f"Code Length: {data['code_length']}")
        print(f"Duration: {data['duration_seconds']}s")
        print(f"Model: {data['model']}")
        print(f"Mock Response: {data['mock']}")
        print(f"From Cache: {data.get('from_cache', False)}")
        print(f"\nExplanation Preview:")
        print(data['explanation'][:300] + "...")
        print(f"✅ Code explanation successful")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def test_code_summarization():
    """Test code summarization endpoint"""
    print_section("Testing Code Summarization")
    
    code = """
class DataProcessor:
    def __init__(self, data_source):
        self.data_source = data_source
        self.processed_data = []
    
    def load_data(self):
        # Load data from source
        pass
    
    def process(self):
        # Process the data
        pass
    
    def save_results(self, output_path):
        # Save processed results
        pass
"""
    
    payload = {
        "content": code,
        "language": "python",
        "context": "DataProcessor",
        "summary_type": "class"
    }
    
    print("Sending class code for summarization...")
    response = requests.post(f"{BASE_URL}/api/v1/ai/summarize", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nLanguage: {data['language']}")
        print(f"Summary Type: {data['summary_type']}")
        print(f"Context: {data['context']}")
        print(f"Duration: {data['duration_seconds']}s")
        print(f"\nSummary Preview:")
        print(data['summary'][:300] + "...")
        print(f"✅ Code summarization successful")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def test_documentation_generation():
    """Test documentation generation endpoint"""
    print_section("Testing Documentation Generation")
    
    code = """
def process_user_data(user_id, data_dict, validate=True):
    # Process user data
    return processed_data
"""
    
    payload = {
        "code": code,
        "language": "python",
        "doc_style": "google"
    }
    
    print("Sending code for documentation generation...")
    response = requests.post(f"{BASE_URL}/api/v1/ai/document", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nLanguage: {data['language']}")
        print(f"Doc Style: {data.get('doc_style', 'N/A')}")
        print(f"Duration: {data['duration_seconds']}s")
        print(f"\nDocumentation Preview:")
        print(data['documentation'][:300] + "...")
        print(f"✅ Documentation generation successful")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def test_cache_functionality():
    """Test caching mechanism"""
    print_section("Testing Cache Functionality")
    
    code = "def test(): pass"
    payload = {"code": code, "language": "python"}
    
    # First request (should not be cached)
    print("Making first request (should miss cache)...")
    start = time.time()
    response1 = requests.post(f"{BASE_URL}/api/v1/ai/explain", json=payload)
    duration1 = time.time() - start
    
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"First request duration: {duration1:.3f}s")
        print(f"From cache: {data1.get('from_cache', False)}")
    
    # Second request (should be cached)
    print("\nMaking second request (should hit cache)...")
    start = time.time()
    response2 = requests.post(f"{BASE_URL}/api/v1/ai/explain", json=payload)
    duration2 = time.time() - start
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"Second request duration: {duration2:.3f}s")
        print(f"From cache: {data2.get('from_cache', False)}")
        
        if data2.get('from_cache'):
            print(f"✅ Cache is working! Second request was {duration1/duration2:.1f}x faster")
            return True
        else:
            print(f"⚠️  Cache might not be working as expected")
            return False
    
    return False


def test_cache_stats():
    """Test cache statistics endpoint"""
    print_section("Testing Cache Statistics")
    
    response = requests.get(f"{BASE_URL}/api/v1/ai/cache/stats")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nCache Statistics:")
        print(f"  Total Requests: {data['total_requests']}")
        print(f"  Hits: {data['hits']}")
        print(f"  Misses: {data['misses']}")
        print(f"  Hit Rate: {data['hit_rate_percent']}%")
        print(f"  Cached Items: {data['cached_items']}")
        print(f"  Total Size: {data['total_size_mb']} MB")
        print(f"  TTL: {data['ttl_hours']} hours")
        print(f"✅ Cache statistics retrieved")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False


def test_multi_language_support():
    """Test multi-language support"""
    print_section("Testing Multi-Language Support")
    
    test_cases = [
        {
            "language": "python",
            "code": "def hello():\n    print('Hello')"
        },
        {
            "language": "javascript",
            "code": "function hello() {\n    console.log('Hello');\n}"
        },
        {
            "language": "typescript",
            "code": "function hello(): void {\n    console.log('Hello');\n}"
        },
        {
            "language": "java",
            "code": "public class Hello {\n    public void hello() {\n        System.out.println(\"Hello\");\n    }\n}"
        }
    ]
    
    results = []
    for test_case in test_cases:
        print(f"\nTesting {test_case['language']}...")
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/explain",
            json=test_case
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ {test_case['language']}: Success (duration: {data['duration_seconds']}s)")
            results.append(True)
        else:
            print(f"  ❌ {test_case['language']}: Failed")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n✅ Multi-language support: {success_rate:.0f}% success rate")
    return all(results)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  STAGE 4 AI INTEGRATION TEST SUITE")
    print("="*60)
    
    tests = [
        ("API Info", test_api_info),
        ("AI Health Check", test_ai_health),
        ("Code Explanation", test_code_explanation),
        ("Code Summarization", test_code_summarization),
        ("Documentation Generation", test_documentation_generation),
        ("Cache Functionality", test_cache_functionality),
        ("Cache Statistics", test_cache_stats),
        ("Multi-Language Support", test_multi_language_support),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with exception: {e}")
            results[test_name] = False
        
        time.sleep(0.5)  # Small delay between tests
    
    # Print summary
    print_section("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print(f"{'='*60}\n")
    
    return passed == total


if __name__ == "__main__":
    print("\nMake sure the server is running on http://localhost:8000")
    print("Press Enter to start tests...")
    input()
    
    success = run_all_tests()
    
    if success:
        print("🎉 All tests passed! Stage 4 implementation is complete.")
    else:
        print("⚠️  Some tests failed. Please review the output above.")

# Made with Bob
