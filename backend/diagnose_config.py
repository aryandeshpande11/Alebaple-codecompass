"""Diagnose configuration loading"""
import os
import sys

print("="*70)
print("CONFIGURATION DIAGNOSTICS")
print("="*70)

# Check current directory
print(f"\n1. Current Directory: {os.getcwd()}")

# Check if .env exists
env_path = os.path.join(os.getcwd(), ".env")
print(f"\n2. Looking for .env at: {env_path}")
print(f"   .env exists: {os.path.exists(env_path)}")

# Try to load with python-dotenv
print("\n3. Loading with python-dotenv:")
from dotenv import load_dotenv
load_dotenv()
print(f"   WATSONX_API_KEY: {os.getenv('WATSONX_API_KEY', 'NOT FOUND')[:20]}...")
print(f"   WATSONX_PROJECT_ID: {os.getenv('WATSONX_PROJECT_ID', 'NOT FOUND')}")
print(f"   USE_MOCK_RESPONSES: {os.getenv('USE_MOCK_RESPONSES', 'NOT FOUND')}")

# Try to load with pydantic_settings
print("\n4. Loading with pydantic_settings:")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.core.ai_config import WatsonxAIConfig

config = WatsonxAIConfig()
print(f"   watsonx_api_key: {config.watsonx_api_key[:20] if config.watsonx_api_key else 'EMPTY'}...")
print(f"   watsonx_project_id: {config.watsonx_project_id or 'EMPTY'}")
print(f"   use_mock_responses: {config.use_mock_responses}")
print(f"   is_configured(): {config.is_configured()}")

print("\n5. Environment variables in os.environ:")
for key in ['WATSONX_API_KEY', 'WATSONX_PROJECT_ID', 'USE_MOCK_RESPONSES']:
    value = os.environ.get(key, 'NOT SET')
    if key == 'WATSONX_API_KEY' and value != 'NOT SET':
        value = value[:20] + '...'
    print(f"   {key}: {value}")

print("\n" + "="*70)

# Made with Bob
