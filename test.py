"""
Basic test script to verify Person 1's work
Run this to test your API implementation
"""
import requests
import json
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_test(name: str):
    """Print test name"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST: {name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")


def print_success(message: str):
    """Print success message"""
    print(f"{GREEN}✅ {message}{RESET}")


def print_error(message: str):
    """Print error message"""
    print(f"{RED}❌ {message}{RESET}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {message}{RESET}")


def print_response(response: requests.Response):
    """Pretty print response"""
    print(f"\nStatus Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def test_root_endpoint():
    """Test 1: Root endpoint"""
    print_test("Root Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            if "message" in data and "version" in data:
                print_success("Root endpoint working correctly!")
                return True
            else:
                print_error("Response missing required fields")
                return False
        else:
            print_error(f"Expected status 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        print_warning("Make sure the server is running with: python -m backend.main")
        return False


def test_health_endpoint():
    """Test 2: Health check endpoint"""
    print_test("Health Check Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print_response(response)
        
        # Note: This will fail until Person 2 implements chat_service
        if response.status_code in [200, 503]:
            print_success("Health endpoint responding (will show unhealthy until chat_service is implemented)")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_sessions_list():
    """Test 3: List sessions endpoint"""
    print_test("List Sessions Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/sessions")
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            if "sessions" in data and "count" in data:
                print_success(f"Sessions endpoint working! Found {data['count']} sessions")
                return True
            else:
                print_error("Response missing required fields")
                return False
        else:
            print_error(f"Expected status 200, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_chat_validation():
    """Test 4: Chat endpoint validation (will fail without chat_service)"""
    print_test("Chat Endpoint Validation")
    
    # Test with invalid request (empty prompt)
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",
            json={
                "prompt": "",
                "session_id": "test_session_123"
            }
        )
        print_response(response)
        
        if response.status_code == 422:  # Validation error
            print_success("Request validation working correctly!")
            return True
        else:
            print_error(f"Expected status 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_session_info_not_found():
    """Test 5: Session info endpoint - not found case"""
    print_test("Session Info Endpoint (Not Found)")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/sessions/nonexistent_session/info")
        print_response(response)
        
        if response.status_code == 404:
            print_success("404 handling working correctly!")
            return True
        else:
            print_error(f"Expected status 404, got {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_api_docs():
    """Test 6: API documentation"""
    print_test("API Documentation")
    
    try:
        # Test Swagger docs
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print_success("Swagger docs accessible at http://localhost:8000/docs")
        else:
            print_error("Swagger docs not accessible")
            
        # Test ReDoc
        response = requests.get(f"{BASE_URL}/redoc")
        if response.status_code == 200:
            print_success("ReDoc accessible at http://localhost:8000/redoc")
            return True
        else:
            print_error("ReDoc not accessible")
            return False
            
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}GEMMA CHATBOT API - PERSON 1 TESTING{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_endpoint),
        ("List Sessions", test_sessions_list),
        ("Chat Validation", test_chat_validation),
        ("Session Not Found", test_session_info_not_found),
        ("API Documentation", test_api_docs),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST SUMMARY{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"{status} - {test_name}")
    
    print(f"\n{BLUE}Results: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 All tests passed! Person 1 work is complete!{RESET}")
    else:
        print(f"\n{YELLOW}⚠️  Some tests failed. Check the output above.{RESET}")
    
    print(f"\n{YELLOW}Note: Chat functionality will not work until Person 2 implements chat_service.py{RESET}")


if __name__ == "__main__":
    print(f"\n{YELLOW}Make sure your API is running on http://localhost:8000{RESET}")
    print(f"{YELLOW}Start it with: python -m backend.main{RESET}\n")
    
    input("Press Enter to start testing...")
    
    run_all_tests()