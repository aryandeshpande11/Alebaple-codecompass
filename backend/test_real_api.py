"""
Quick Test Script for Real IBM watsonx.ai API Integration
Run this after adding your Project ID to .env file
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def test_ai_health():
    """Test AI service health"""
    print_header("TEST 1: AI Service Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ai/health")
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("\n[PASS] AI service is healthy!")
            if data.get("mock_mode") == False:
                print("[INFO] Using REAL IBM watsonx.ai API")
            else:
                print("[WARN] Still in mock mode - check .env file")
            return True
        else:
            print("\n[FAIL] AI service health check failed")
            return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

def test_code_explanation():
    """Test code explanation with real API"""
    print_header("TEST 2: Code Explanation (Real API)")
    
    sample_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/ai/explain",
            json={
                "code": sample_code,
                "language": "python"
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nExplanation:")
            print(f"{data.get('explanation', 'No explanation')}")
            print(f"\nModel Used: {data.get('model', 'Unknown')}")
            print(f"From Cache: {data.get('from_cache', False)}")
            print(f"Timestamp: {data.get('timestamp', 'Unknown')}")
            print("\n[PASS] Code explanation successful!")
            return True
        else:
            print(f"\n[FAIL] Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

def test_cache_stats():
    """Test cache statistics"""
    print_header("TEST 3: Cache Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/ai/cache/stats")
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"\nCache Stats:")
        print(f"  Total Requests: {data.get('total_requests', 0)}")
        print(f"  Cache Hits: {data.get('hits', 0)}")
        print(f"  Cache Misses: {data.get('misses', 0)}")
        print(f"  Hit Rate: {data.get('hit_rate_percent', 0)}%")
        print(f"  Cached Items: {data.get('cached_items', 0)}")
        
        if response.status_code == 200:
            print("\n[PASS] Cache statistics retrieved!")
            return True
        else:
            print("\n[FAIL] Failed to get cache stats")
            return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  IBM WATSONX.AI REAL API INTEGRATION TEST")
    print("="*70)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Testing against: {BASE_URL}")
    print("="*70)
    
    results = []
    
    # Test 1: Health Check
    results.append(("AI Health Check", test_ai_health()))
    
    # Test 2: Code Explanation
    results.append(("Code Explanation", test_code_explanation()))
    
    # Test 3: Cache Stats
    results.append(("Cache Statistics", test_cache_stats()))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! Real API integration is working!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("="*70)

if __name__ == "__main__":
    main()

# Made with Bob
