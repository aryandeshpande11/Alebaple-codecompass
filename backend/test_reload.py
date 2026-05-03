"""Test the reload endpoint"""
import requests
import time

print("="*70)
print("TESTING AI SERVICE RELOAD")
print("="*70)

# Wait for server to reload
print("\nWaiting 3 seconds for server auto-reload...")
time.sleep(3)

# Test reload endpoint
print("\n1. Calling reload endpoint...")
try:
    response = requests.post("http://localhost:8000/api/v1/ai/reload")
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Message: {data.get('message')}")
        print(f"   Mock Mode: {data.get('mock_mode')}")
        print(f"   Configured: {data.get('configured')}")
        print(f"   Has API Key: {data.get('has_api_key')}")
        print(f"   Has Project ID: {data.get('has_project_id')}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test health endpoint
print("\n2. Testing AI health after reload...")
try:
    response = requests.get("http://localhost:8000/api/v1/ai/health")
    data = response.json()
    print(f"   Status: {data.get('status')}")
    print(f"   Mock Mode: {data.get('mock_mode')}")
    print(f"   Model: {data.get('model')}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*70)

# Made with Bob
