"""Test what configuration the running server actually has"""
import requests

print("="*70)
print("SERVER CONFIGURATION DIAGNOSTIC")
print("="*70)

# Test health endpoint to see current config
print("\n1. Current Server Configuration:")
try:
    response = requests.get("http://localhost:8000/api/v1/ai/health")
    data = response.json()
    print(f"   Status: {data.get('status')}")
    print(f"   Mock Mode: {data.get('mock_mode')}")
    print(f"   Configured: {data.get('configured')}")
    print(f"   Model: {data.get('model')}")
    
    if data.get('mock_mode'):
        print("\n   ⚠️  SERVER IS IN MOCK MODE")
        print("   This means the AI service was initialized without real credentials")
    else:
        print("\n   ✓ SERVER IS IN REAL API MODE")
        
except Exception as e:
    print(f"   Error: {e}")

# Check if server can see the environment variables
print("\n2. Testing if server process has access to .env:")
print("   (The server needs to be started FROM the backend directory)")
print("   Current server working directory should be:")
print("   C:\\Users\\HP\\OneDrive\\Desktop\\ibm\\Alebaple-codecompass\\backend")

# Test a simple explanation to see the response
print("\n3. Testing AI Explanation (to see if it's mock or real):")
try:
    response = requests.post(
        "http://localhost:8000/api/v1/ai/explain",
        json={
            "code": "def hello(): return 'world'",
            "language": "python"
        }
    )
    data = response.json()
    print(f"   Status: SUCCESS")
    print(f"   Mock: {data.get('mock', 'unknown')}")
    print(f"   Explanation length: {len(data.get('explanation', ''))} chars")
    
    if data.get('mock'):
        print("\n   ⚠️  Response is from MOCK API")
    else:
        print("\n   ✓ Response is from REAL IBM watsonx.ai API")
        
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*70)
print("DIAGNOSIS:")
print("="*70)
print("""
If the server is in mock mode, it means:
1. The server was started before .env was created/updated, OR
2. The server is not running from the backend directory, OR
3. The .env file is not being loaded by pydantic_settings

SOLUTION:
- Make sure you're in the backend directory
- Stop the server (Ctrl+C in the terminal showing uvicorn)
- Start fresh: python -m uvicorn app.main:app --reload --port 8000
- The server MUST see this on startup:
  INFO:ibm_watsonx_ai.client:Client successfully initialized
""")
print("="*70)

# Made with Bob
