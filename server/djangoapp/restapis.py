# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
import json # Added for json.dumps for logging, if not already present

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")

def analyze_review_sentiments(text): # Assuming this one is okay for now or will be addressed later if needed
    request_url = sentiment_analyzer_url+"analyze/"+text
    default_response = {"sentiment": "N/A", "error": "Sentiment analysis failed"} # More robust return
    try:
        api_response = requests.get(request_url, timeout=5)
        api_response.raise_for_status()
        parsed_json = api_response.json()
        print(f"Sentiment API response for '{text}': {parsed_json}, type: {type(parsed_json)}") # Optional debug print
        return parsed_json
    except requests.exceptions.RequestException as err:
        print(f"Network exception for sentiment analysis: {err}")
        return default_response 
    except json.JSONDecodeError as err:
        print(f"JSON decode error for sentiment analysis: {err} - Response was: {api_response.text if 'api_response' in locals() else 'N/A'}")
        return default_response
    except Exception as err:
        print(f"Unexpected error in analyze_review_sentiments: {type(err).__name__} - {err}")
        return default_response

def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    print(f"--- Attempting to POST review to: {request_url}")
    try:
        data_to_log = json.dumps(data_dict)
    except TypeError:
        data_to_log = str(data_dict)
    print(f"--- Review data being sent: {data_to_log}")
    
    try:
        api_response = requests.post(request_url, json=data_dict, timeout=10)
        print(f"--- Node.js backend response status code for insert_review: {api_response.status_code}")
        print(f"--- Node.js backend response text for insert_review: {api_response.text}")
        
        try:
            parsed_json_response = api_response.json()
            print(f"--- Node.js backend parsed JSON response for insert_review: {parsed_json_response}")
            return parsed_json_response
        except json.JSONDecodeError as json_err:
            print(f"--- FAILED to parse JSON from Node.js backend for insert_review: {json_err}")
            print(f"--- Original response text was: {api_response.text}")
            return {"error": "Invalid JSON response from backend", "details": api_response.text, "status_code": api_response.status_code}

    except requests.exceptions.Timeout:
        print(f"--- Timeout occurred when POSTing review to {request_url}")
        return {"error": "Timeout when posting review", "details": "Request timed out"}
    except requests.exceptions.RequestException as req_err:
        print(f"--- Network exception occurred when POSTing review: {req_err}")
        return {"error": "Network exception when posting review", "details": str(req_err)}
    except Exception as e:
        print(f"--- An unexpected error occurred in post_review: {type(e).__name__} - {e}")
        return {"error": "Unexpected error in post_review", "details": str(e)}