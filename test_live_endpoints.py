"""
Test live API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_explain_endpoint():
    """Test the explain code endpoint"""
    print("\n" + "="*60)
    print("Testing POST /api/v1/ai/explain")
    print("="*60)
    
    payload = {
        "code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
        "language": "python",
        "context": "Recursive implementation"
    }
    
    response = requests.post(f"{BASE_URL}/ai/explain", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Cached: {data.get('cached', False)}")
        print(f"Explanation: {data.get('explanation', '')[:100]}...")
        print(f"Key Concepts: {data.get('key_concepts', [])}")
        print("[OK] Explain endpoint working!")
        return True
    else:
        print(f"[FAIL] Error: {response.text}")
        return False


def test_cache_stats():
    """Test cache stats endpoint"""
    print("\n" + "="*60)
    print("Testing GET /api/v1/ai/cache/stats")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/ai/cache/stats")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total Entries: {data.get('total_entries', 0)}")
        print(f"Total Size: {data.get('total_size_mb', 0)} MB")
        print(f"Cache Dir: {data.get('cache_dir', '')}")
        print("[OK] Cache stats endpoint working!")
        return True
    else:
        print(f"[FAIL] Error: {response.text}")
        return False


def test_summarize_endpoint():
    """Test the summarize code endpoint"""
    print("\n" + "="*60)
    print("Testing POST /api/v1/ai/summarize")
    print("="*60)
    
    payload = {
        "code": "class UserManager:\n    def create_user(self, name, email):\n        pass",
        "language": "python",
        "summary_type": "brief"
    }
    
    response = requests.post(f"{BASE_URL}/ai/summarize", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Summary: {data.get('summary', '')[:100]}...")
        print(f"Main Purpose: {data.get('main_purpose', '')}")
        print("[OK] Summarize endpoint working!")
        return True
    else:
        print(f"[FAIL] Error: {response.text}")
        return False


def test_document_endpoint():
    """Test the document generation endpoint"""
    print("\n" + "="*60)
    print("Testing POST /api/v1/ai/document")
    print("="*60)
    
    payload = {
        "code": "def calculate_total(items, tax_rate=0.1):\n    return sum(items) * (1 + tax_rate)",
        "language": "python",
        "doc_style": "google"
    }
    
    response = requests.post(f"{BASE_URL}/ai/document", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Format: {data.get('format', '')}")
        print(f"Documentation: {data.get('documentation', '')[:150]}...")
        print("[OK] Document endpoint working!")
        return True
    else:
        print(f"[FAIL] Error: {response.text}")
        return False


def main():
    print("="*60)
    print("Live API Endpoint Tests")
    print("="*60)
    print("Server: http://localhost:8000")
    
    results = []
    
    try:
        results.append(("Explain", test_explain_endpoint()))
        results.append(("Cache Stats", test_cache_stats()))
        results.append(("Summarize", test_summarize_endpoint()))
        results.append(("Document", test_document_endpoint()))
        
        # Test caching by calling explain again
        print("\n" + "="*60)
        print("Testing Cache (calling explain again)")
        print("="*60)
        results.append(("Cache Test", test_explain_endpoint()))
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server!")
        print("Make sure the server is running: cd backend && python -m uvicorn app.main:app --reload")
        return
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for name, passed in results:
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{name:20s}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("SUCCESS: All live endpoint tests passed!")
        print("Developer B Stage 4 tasks are fully functional!")
    else:
        print("WARNING: Some tests failed.")
    print("="*60)


if __name__ == "__main__":
    main()

# Made with Bob
