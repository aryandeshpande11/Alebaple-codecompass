"""Check environment variables"""
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("WATSONX_API_KEY", "")
project_id = os.getenv("WATSONX_PROJECT_ID", "")
mock_mode = os.getenv("USE_MOCK_RESPONSES", "true")

print("="*70)
print("ENVIRONMENT CONFIGURATION CHECK")
print("="*70)
print(f"API Key: {api_key[:20]}... (length: {len(api_key)})")
print(f"Project ID: {project_id}")
print(f"Mock Mode: {mock_mode}")
print(f"Mock Mode (bool): {mock_mode.lower() == 'true'}")
print("="*70)

if api_key and project_id and mock_mode.lower() == "false":
    print("\nCONFIGURATION: Ready for real API")
    print("ACTION: Restart server to activate")
else:
    print("\nCONFIGURATION: Check .env file")

# Made with Bob
