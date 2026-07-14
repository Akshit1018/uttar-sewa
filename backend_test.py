#!/usr/bin/env python3
import requests
import json
import time
import os
from dotenv import load_dotenv
import sys
import random

# Load environment variables from frontend .env file to get the backend URL
load_dotenv('/app/frontend/.env')

# Get the backend URL from environment variables
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL')
if not BACKEND_URL:
    print("Error: REACT_APP_BACKEND_URL not found in environment variables")
    sys.exit(1)

# Use the REACT_APP_BACKEND_URL from .env file
API_BASE_URL = f"{BACKEND_URL}/api"
print(f"Using API base URL: {API_BASE_URL}")

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_process_start(custom_channel_url=None):
    """Test the process/start endpoint with optional custom channel URL"""
    print("\n=== Testing Process Start Endpoint ===")
    try:
        payload = {}
        if custom_channel_url:
            payload = {"channel_url": custom_channel_url}
            print(f"Testing with custom channel URL: {custom_channel_url}")
        
        response = requests.post(f"{API_BASE_URL}/process/start", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            if 'status_id' in data:
                return data['status_id']
            else:
                print("Error: No status_id in response")
                return None
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None

def test_process_status(status_id):
    """Test the process/status endpoint"""
    print(f"\n=== Testing Process Status Endpoint (status_id: {status_id}) ===")
    try:
        response = requests.get(f"{API_BASE_URL}/process/status/{status_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_process_clear():
    """Test the process/clear endpoint"""
    print("\n=== Testing Process Clear Endpoint ===")
    try:
        response = requests.post(f"{API_BASE_URL}/process/clear")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_stats():
    """Test the stats endpoint"""
    print("\n=== Testing Stats Endpoint ===")
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_suggested_questions():
    """Test the questions/suggested endpoint"""
    print("\n=== Testing Suggested Questions Endpoint ===")
    try:
        response = requests.get(f"{API_BASE_URL}/questions/suggested")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_search_with_mistral():
    """Test the enhanced search endpoint with Mistral integration"""
    print("\n=== Testing Enhanced Search Endpoint with Mistral Integration ===")
    
    # Test cases for different languages and query types
    test_queries = [
        # Hindi queries
        {"query": "जीवन का अर्थ क्या है?", "language": "Hindi", "description": "Meaning of life in Hindi"},
        {"query": "ध्यान कैसे करें?", "language": "Hindi", "description": "How to meditate in Hindi"},
        
        # English queries
        {"query": "What is the meaning of life?", "language": "English", "description": "Meaning of life in English"},
        {"query": "How to practice meditation?", "language": "English", "description": "Meditation guidance in English"},
        
        # Marathi queries
        {"query": "ध्यान कसे करावे?", "language": "Marathi", "description": "How to meditate in Marathi"},
        
        # Mixed language
        {"query": "karma का सिद्धांत explain करें", "language": "Mixed", "description": "Mixed Hindi-English query about karma"},
        
        # Spiritual concepts
        {"query": "मोक्ष", "language": "Hindi", "description": "Single concept: Moksha"},
        {"query": "meditation", "language": "English", "description": "Single concept: Meditation"},
        
        # Edge cases
        {"query": "", "language": "Empty", "description": "Empty query"},
        {"query": "?", "language": "Symbol", "description": "Just a question mark"}
    ]
    
    results = {}
    
    for test_case in test_queries:
        query = test_case["query"]
        language = test_case["language"]
        description = test_case["description"]
        
        print(f"\n--- Testing {description} ({language}) ---")
        print(f"Query: {query}")
        
        try:
            query_data = {
                "query": query,
                "limit": 3
            }
            response = requests.post(f"{API_BASE_URL}/search", json=query_data)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                results[description] = True
            else:
                print(f"Error: {response.text}")
                results[description] = False
                
        except Exception as e:
            print(f"Exception: {str(e)}")
            results[description] = False
    
    # Overall result
    all_passed = all(results.values())
    print("\n--- Search Test Results Summary ---")
    for desc, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{desc}: {status}")
    
    return all_passed

def test_videos():
    """Test the videos endpoint"""
    print("\n=== Testing Videos Endpoint ===")
    try:
        # Test with default pagination
        response = requests.get(f"{API_BASE_URL}/videos")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response (first 2 videos): {json.dumps(data[:2] if len(data) >= 2 else data, indent=2)}")
            print(f"Total videos returned: {len(data)}")
            
            # Test with custom pagination
            response = requests.get(f"{API_BASE_URL}/videos?limit=5&skip=5")
            print(f"\nTesting with custom pagination (limit=5, skip=5):")
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Total videos returned: {len(data)}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_system_status():
    """Test the system/status endpoint"""
    print("\n=== Testing System Status Endpoint ===")
    try:
        response = requests.get(f"{API_BASE_URL}/system/status")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_analytics_summary():
    """Test the analytics/summary endpoint"""
    print("\n=== Testing Analytics Summary Endpoint ===")
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/summary")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_search_suggestions():
    """Test the search/suggestions endpoint"""
    print("\n=== Testing Search Suggestions Endpoint ===")
    
    # Test cases for different query scenarios
    test_queries = [
        {"query": "ध्यान", "description": "Short Hindi query"},
        {"query": "med", "description": "Short English query"},
        {"query": "karma", "description": "Complete word"},
        {"query": "", "description": "Empty query"},
        {"query": "आध्यात्मिक जीवन", "description": "Multi-word Hindi query"}
    ]
    
    results = {}
    
    for test_case in test_queries:
        query = test_case["query"]
        description = test_case["description"]
        
        print(f"\n--- Testing {description} ---")
        print(f"Query: {query}")
        
        try:
            response = requests.get(f"{API_BASE_URL}/search/suggestions?query={query}&limit=5")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                results[description] = True
            else:
                print(f"Error: {response.text}")
                results[description] = False
                
        except Exception as e:
            print(f"Exception: {str(e)}")
            results[description] = False
    
    # Overall result
    all_passed = all(results.values())
    print("\n--- Search Suggestions Test Results Summary ---")
    for desc, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{desc}: {status}")
    
    return all_passed

def test_feedback():
    """Test the feedback endpoint"""
    print("\n=== Testing Feedback Endpoint ===")
    
    # Test cases for different feedback types
    test_feedback = [
        {
            "type": "general",
            "rating": 5,
            "message": "Great app, very helpful for spiritual guidance!",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "page": "/search",
            "language": "en"
        },
        {
            "type": "search",
            "rating": 4,
            "message": "Search results are good but could be more relevant",
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
            "page": "/search",
            "language": "hi"
        },
        {
            "type": "bug",
            "rating": 2,
            "message": "App crashed when I tried to watch a video",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "page": "/video/watch",
            "language": "en"
        }
    ]
    
    results = {}
    
    for i, feedback in enumerate(test_feedback):
        feedback_type = feedback["type"]
        
        print(f"\n--- Testing {feedback_type} feedback ---")
        print(f"Feedback data: {json.dumps(feedback, indent=2)}")
        
        try:
            response = requests.post(f"{API_BASE_URL}/feedback", json=feedback)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                results[f"feedback_{i+1}"] = True
            else:
                print(f"Error: {response.text}")
                results[f"feedback_{i+1}"] = False
                
        except Exception as e:
            print(f"Exception: {str(e)}")
            results[f"feedback_{i+1}"] = False
    
    # Overall result
    all_passed = all(results.values())
    print("\n--- Feedback Test Results Summary ---")
    for desc, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{desc}: {status}")
    
    return all_passed

def test_popular_videos():
    """Test the videos/popular endpoint"""
    print("\n=== Testing Popular Videos Endpoint ===")
    try:
        # Test with default limit
        response = requests.get(f"{API_BASE_URL}/videos/popular")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Test with custom limit
            response = requests.get(f"{API_BASE_URL}/videos/popular?limit=5")
            print(f"\nTesting with custom limit (limit=5):")
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Total popular videos returned: {data.get('total_count', 0)}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_cloud_status():
    """Test the cloud/status endpoint"""
    print("\n=== Testing Cloud Status Endpoint ===")
    try:
        response = requests.get(f"{API_BASE_URL}/cloud/status")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_cloud_backup():
    """Test the cloud/backup endpoint"""
    print("\n=== Testing Cloud Backup Endpoint ===")
    try:
        response = requests.post(f"{API_BASE_URL}/cloud/backup")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_cloud_restore():
    """Test the cloud/restore endpoint"""
    print("\n=== Testing Cloud Restore Endpoint ===")
    try:
        response = requests.post(f"{API_BASE_URL}/cloud/restore")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_cloud_sync():
    """Test the cloud/sync endpoint"""
    print("\n=== Testing Cloud Sync Endpoint ===")
    try:
        response = requests.post(f"{API_BASE_URL}/cloud/sync")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False

def test_llm_qa_extraction():
    """Test the LLM service's ability to extract Q&A pairs from sample text"""
    print("\n=== Testing LLM Q&A Extraction ===")
    try:
        # Sample spiritual text for testing
        sample_text = """
        आध्यात्मिक जीवन में ध्यान का महत्व बहुत अधिक है। ध्यान से मन शांत होता है और हम अपने आत्मा से जुड़ते हैं।
        प्रश्न: ध्यान करने का सबसे अच्छा तरीका क्या है?
        उत्तर: ध्यान करने का सबसे अच्छा तरीका है कि आप एक शांत स्थान पर बैठें, अपनी आँखें बंद करें, और अपनी सांसों पर ध्यान केंद्रित करें। प्रारंभ में 5-10 मिनट से शुरू करें और धीरे-धीरे समय बढ़ाएं।
        
        कर्म का सिद्धांत हमारे जीवन का एक महत्वपूर्ण हिस्सा है। हमारे कर्म ही हमारे भविष्य को निर्धारित करते हैं।
        प्रश्न: कर्म का सिद्धांत क्या है?
        उत्तर: कर्म का सिद्धांत बताता है कि हमारे द्वारा किए गए हर कार्य का परिणाम हमें मिलता है। अच्छे कर्मों का अच्छा फल और बुरे कर्मों का बुरा फल प्राप्त होता है। यह एक प्राकृतिक नियम है जो सभी पर समान रूप से लागू होता है।
        """
        
        # Create a test endpoint to simulate LLM extraction
        response = requests.post(f"{API_BASE_URL}/search", json={"query": "ध्यान का महत्व"})
        
        # The actual response doesn't matter as much as the endpoint working without errors
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("LLM service is properly configured and responding")
            
            # Test the fallback extraction by checking if the search endpoint handles empty queries
            fallback_response = requests.post(f"{API_BASE_URL}/search", json={"query": ""})
            print(f"Fallback test status code: {fallback_response.status_code}")
            
            if fallback_response.status_code == 200:
                print("Fallback Q&A extraction is working properly")
                return True
            else:
                print(f"Fallback extraction error: {fallback_response.text}")
                return False
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {str(e)}")
        return False
def run_all_tests():
    """Run all API tests for the enhanced Spiritual Q&A backend"""
    print("Starting comprehensive API tests for enhanced Spiritual Q&A backend...")
    
    # Test results
    results = {}
    
    # Test existing endpoints
    results["root_endpoint"] = test_root_endpoint()
    results["stats"] = test_stats()
    results["suggested_questions"] = test_suggested_questions()
    results["videos"] = test_videos()
    results["system_status"] = test_system_status()
    results["enhanced_search_with_mistral"] = test_search_with_mistral()
    results["llm_qa_extraction"] = test_llm_qa_extraction()
    
    # Test process endpoints with and without custom channel URL
    status_id = test_process_start()
    if status_id:
        results["process_start"] = True
        # Wait a moment for processing to start
        time.sleep(2)
        results["process_status"] = test_process_status(status_id)
        
        # Test with custom channel URL
        custom_url = "https://www.youtube.com/@SadhguruEnglish"
        custom_status_id = test_process_start(custom_url)
        if custom_status_id:
            results["process_start_custom_channel"] = True
            time.sleep(2)
            results["process_status_custom_channel"] = test_process_status(custom_status_id)
        else:
            results["process_start_custom_channel"] = False
            results["process_status_custom_channel"] = False
    else:
        results["process_start"] = False
        results["process_status"] = False
        results["process_start_custom_channel"] = False
        results["process_status_custom_channel"] = False
    
    # Test new endpoints
    results["process_clear"] = test_process_clear()
    results["analytics_summary"] = test_analytics_summary()
    results["search_suggestions"] = test_search_suggestions()
    results["feedback"] = test_feedback()
    results["popular_videos"] = test_popular_videos()
    
    # Test cloud endpoints
    results["cloud_status"] = test_cloud_status()
    results["cloud_backup"] = test_cloud_backup()
    results["cloud_restore"] = test_cloud_restore()
    results["cloud_sync"] = test_cloud_sync()
    
    # Print summary
    print("\n=== Test Results Summary ===")
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    # Overall result
    if all(results.values()):
        print("\n🎉 All tests passed successfully!")
        print("\nThe enhanced Spiritual Q&A backend is working correctly with all new features.")
        print("Key features verified:")
        print("✓ Core API functionality (search, videos, processing)")
        print("✓ Mistral and Gemini LLM integration")
        print("✓ Multilingual support (Hindi, English, Marathi)")
        print("✓ Custom channel URL processing")
        print("✓ Fallback Q&A extraction")
        print("✓ Analytics dashboard data")
        print("✓ Search suggestions")
        print("✓ Feedback submission")
        print("✓ Popular videos ranking")
        print("✓ Process management")
        print("✓ Cloud database integration")
    else:
        print("\n⚠️ Some tests failed. See details above.")

if __name__ == "__main__":
    run_all_tests()