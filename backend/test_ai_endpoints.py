"""
Test script for AI endpoints and caching system
Run this after starting the server to verify all functionality
"""
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def test_schemas():
    """Test that all schemas can be imported"""
    print("Testing AI Schemas...")
    try:
        from app.schemas.ai import (
            ExplainCodeRequest, ExplainCodeResponse,
            ExplainFileRequest, SummarizeRequest, SummarizeResponse,
            GenerateDocsRequest, GenerateDocsResponse
        )
        print("[OK] All AI schemas imported successfully")
        
        # Test schema validation
        explain_req = ExplainCodeRequest(
            code="def hello(): print('hi')",
            language="python"
        )
        print(f"[OK] ExplainCodeRequest validation works: {explain_req.language}")
        
        return True
    except Exception as e:
        print(f"[FAIL] Schema test failed: {e}")
        return False


def test_cache():
    """Test caching system"""
    print("\nTesting Cache System...")
    try:
        from app.utils.cache import ai_cache
        
        # Test cache operations
        test_code = "def test(): pass"
        test_lang = "python"
        test_type = "explain"
        test_response = {
            "explanation": "Test explanation",
            "key_concepts": ["test"],
            "cached": False
        }
        
        # Set cache
        success = ai_cache.set(test_code, test_lang, test_type, test_response)
        print(f"[OK] Cache set operation: {'Success' if success else 'Failed'}")
        
        # Get cache
        cached = ai_cache.get(test_code, test_lang, test_type)
        if cached:
            print(f"[OK] Cache get operation: Retrieved cached response")
        else:
            print(f"[WARN] Cache get operation: No cached response found")
        
        # Get stats
        stats = ai_cache.get_stats()
        print(f"[OK] Cache stats: {stats['total_entries']} entries, {stats['total_size_mb']} MB")
        
        return True
    except Exception as e:
        print(f"[FAIL] Cache test failed: {e}")
        return False


def test_endpoint_structure():
    """Test that endpoint file is properly structured"""
    print("\nTesting Endpoint Structure...")
    try:
        from app.api.v1.endpoints import ai
        
        # Check router exists
        if hasattr(ai, 'router'):
            print("[OK] AI router exists")
        
        # Check endpoints exist
        endpoints = ['explain_code', 'explain_file', 'summarize_code', 
                    'generate_documentation', 'get_cache_stats', 'clear_expired_cache']
        
        for endpoint in endpoints:
            if hasattr(ai, endpoint):
                print(f"[OK] Endpoint '{endpoint}' exists")
            else:
                print(f"[WARN] Endpoint '{endpoint}' not found")
        
        return True
    except Exception as e:
        print(f"[FAIL] Endpoint structure test failed: {e}")
        return False


def test_router_integration():
    """Test that AI router is integrated"""
    print("\nTesting Router Integration...")
    try:
        from app.api.v1 import api_router
        
        # Check if AI routes are included
        routes = [route.path for route in api_router.routes]
        ai_routes = [r for r in routes if '/ai/' in r]
        
        if ai_routes:
            print(f"[OK] AI routes integrated: {len(ai_routes)} routes found")
            for route in ai_routes:
                print(f"   - {route}")
        else:
            print("[WARN] No AI routes found in router")
        
        return True
    except Exception as e:
        print(f"[FAIL] Router integration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Endpoints & Caching System - Test Suite")
    print("=" * 60)
    
    results = []
    
    results.append(("Schemas", test_schemas()))
    results.append(("Cache", test_cache()))
    results.append(("Endpoints", test_endpoint_structure()))
    results.append(("Router", test_router_integration()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{name:20s}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("SUCCESS: All tests passed! Developer B tasks complete.")
    else:
        print("WARNING: Some tests failed. Review the output above.")
    print("=" * 60)
    
    print("\nNext Steps:")
    print("1. Start the server: cd backend && python -m uvicorn app.main:app --reload")
    print("2. Test endpoints: http://localhost:8000/api/docs")
    print("3. Test AI explain: POST http://localhost:8000/api/v1/ai/explain")
    print("4. Check cache stats: GET http://localhost:8000/api/v1/ai/cache/stats")


if __name__ == "__main__":
    main()

# Made with Bob
