"""
Final Test - Verify Real IBM watsonx.ai API Integration
"""
import requests

BASE_URL = "http://localhost:8000"

print("="*70)
print("FINAL API INTEGRATION TEST")
print("="*70)

# Test 1: Health Check
print("\n1. Testing AI Health...")
response = requests.get(f"{BASE_URL}/api/v1/ai/health")
data = response.json()
print(f"   Status: {data.get('status')}")
print(f"   Mock Mode: {data.get('mock_mode')}")
print(f"   Model: {data.get('model')}")

if data.get('mock_mode') == False:
    print("\n   SUCCESS! Real IBM watsonx.ai API is active!")
else:
    print("\n   INFO: Still in mock mode - server needs restart")
    print("   Run: Ctrl+C in server terminal, then restart")

# Test 2: Simple Code Explanation
print("\n2. Testing Code Explanation...")
response = requests.post(
    f"{BASE_URL}/api/v1/ai/explain",
    json={
        "code": "def add(a, b): return a + b",
        "language": "python"
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"   Status: SUCCESS")
    print(f"   From Cache: {data.get('from_cache', False)}")
    print(f"   Explanation Length: {len(data.get('explanation', ''))} chars")
    if "mock" in data.get('explanation', '').lower():
        print("   Mode: MOCK")
    else:
        print("   Mode: REAL API")
else:
    print(f"   Status: FAILED ({response.status_code})")

print("\n" + "="*70)
print("Test complete! Check results above.")
print("="*70)

# Made with Bob
