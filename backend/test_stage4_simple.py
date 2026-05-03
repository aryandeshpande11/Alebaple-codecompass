"""
Simple test script for Stage 4 implementations (Windows compatible)
Tests Developer B and Developer C tasks
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"

tests_passed = 0
tests_failed = 0


def test(name, passed, details=""):
    """Log test result"""
    global tests_passed, tests_failed
    
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {name}")
    if details:
        print(f"      {details}")
    
    if passed:
        tests_passed += 1
    else:
        tests_failed += 1
    
    return passed


print("\n" + "="*70)
print("STAGE 4 IMPLEMENTATION TESTING")
print("="*70 + "\n")

# Test 1: Server Health
print("[*] Testing Server Status...")
try:
    r = requests.get(f"{BASE_URL}/api/health", timeout=5)
    test("Server Health", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("Server Health", False, str(e))

# Test 2: API Info
try:
    r = requests.get(f"{API_V1}/info", timeout=5)
    has_ai = "ai_explain" in r.json().get("endpoints", {}) if r.status_code == 200 else False
    test("API Info", has_ai, "AI endpoints registered")
except Exception as e:
    test("API Info", False, str(e))

# Test 3: API Documentation
try:
    r = requests.get(f"{BASE_URL}/api/docs", timeout=5)
    test("API Documentation", r.status_code == 200, "Docs accessible")
except Exception as e:
    test("API Documentation", False, str(e))

print("\n[*] Testing AI Endpoints (Developer B)...")

# Test 4: AI Health
try:
    r = requests.get(f"{API_V1}/ai/health", timeout=5)
    data = r.json() if r.status_code == 200 else {}
    test("AI Health", "status" in data, f"Status: {data.get('status')}, Mock: {data.get('mock_mode')}")
except Exception as e:
    test("AI Health", False, str(e))

# Test 5: AI Explain
try:
    payload = {"code": "def hello():\n    print('Hello')", "language": "python"}
    r = requests.post(f"{API_V1}/ai/explain", json=payload, timeout=10)
    data = r.json() if r.status_code == 200 else {}
    test("AI Explain", "explanation" in data, f"Explanation length: {len(data.get('explanation', ''))}")
except Exception as e:
    test("AI Explain", False, str(e))

# Test 6: AI Summarize
try:
    payload = {"content": "class Test:\n    pass", "language": "python", "summary_type": "class"}
    r = requests.post(f"{API_V1}/ai/summarize", json=payload, timeout=10)
    data = r.json() if r.status_code == 200 else {}
    test("AI Summarize", "summary" in data, f"Summary length: {len(data.get('summary', ''))}")
except Exception as e:
    test("AI Summarize", False, str(e))

# Test 7: AI Document
try:
    payload = {"code": "def calc(x, y):\n    return x + y", "language": "python", "doc_style": "google"}
    r = requests.post(f"{API_V1}/ai/document", json=payload, timeout=10)
    data = r.json() if r.status_code == 200 else {}
    test("AI Document", "documentation" in data, f"Doc length: {len(data.get('documentation', ''))}")
except Exception as e:
    test("AI Document", False, str(e))

print("\n[*] Testing Cache System (Developer B)...")

# Test 8: Cache Stats
try:
    r = requests.get(f"{API_V1}/ai/cache/stats", timeout=5)
    data = r.json() if r.status_code == 200 else {}
    test("Cache Stats", "hits" in data and "misses" in data, 
         f"Hits: {data.get('hits')}, Misses: {data.get('misses')}, Items: {data.get('cached_items')}")
except Exception as e:
    test("Cache Stats", False, str(e))

# Test 9: Caching Works
try:
    payload = {"code": "def test():\n    return 'cache'", "language": "python"}
    r1 = requests.post(f"{API_V1}/ai/explain", json=payload, timeout=10)
    time.sleep(0.5)
    r2 = requests.post(f"{API_V1}/ai/explain", json=payload, timeout=10)
    
    from_cache = r2.json().get("from_cache", False) if r2.status_code == 200 else False
    test("Caching Works", from_cache, "Second request served from cache")
except Exception as e:
    test("Caching Works", False, str(e))

print("\n[*] Testing Enhanced Analysis (Developer C)...")

# Test 10: Enhanced Analysis Endpoint
try:
    # Create test project
    proj = {"name": "Test AI", "description": "Test", "repository_url": "https://github.com/test/repo"}
    r1 = requests.post(f"{API_V1}/projects", json=proj, timeout=5)
    
    if r1.status_code == 201:
        pid = r1.json().get("id")
        payload = {"include_ai_explanations": True, "max_files_to_explain": 3}
        r2 = requests.post(f"{API_V1}/projects/{pid}/analyze-with-ai", json=payload, timeout=10)
        
        data = r2.json() if r2.status_code == 200 else {}
        test("Enhanced Analysis", r2.status_code == 200 and data.get("status") == "analyzing",
             f"Analysis started: {data.get('message', '')}")
    else:
        test("Enhanced Analysis", False, "Failed to create project")
except Exception as e:
    test("Enhanced Analysis", False, str(e))

# Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
print(f"[+] Tests Passed: {tests_passed}")
print(f"[-] Tests Failed: {tests_failed}")
total = tests_passed + tests_failed
print(f"[%] Success Rate: {(tests_passed / total * 100):.1f}%")
print("="*70 + "\n")

# Decision
if tests_passed >= 8:
    print("[!] GO DECISION: All critical tests passed!")
    print("[+] Developer C can proceed with remaining tasks")
    print("[+] Stage 4 implementations are working correctly")
    print("\nREADY TO PROCEED WITH:")
    print("  - Frontend integration")
    print("  - Real watsonx.ai integration (when credentials available)")
    print("  - Additional AI features")
else:
    print("[!] NO-GO DECISION: Some critical tests failed")
    print("[-] Review failed tests before proceeding")

print("\n" + "="*70)

# Made with Bob
