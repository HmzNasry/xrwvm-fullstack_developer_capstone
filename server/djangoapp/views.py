# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
import requests
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request) # Terminate user session
    data = {"userName":""} # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt 
def registration(request): 
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName', '')
            last_name = data.get('lastName', '')
            email = data.get('email', '')

            if not username or not password:
                return JsonResponse({"status": "error", "message": "Username and password are required."}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"status": "error", "message": "An account with this username already exists."}, status=400)
            
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            

            login(request, user) 
            
            return JsonResponse({"status": "success", "userName": username, "message": "Registration successful."}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON format."}, status=400)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return JsonResponse({"status": "error", "message": f"An error occurred: {e}"}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST method is allowed for registration."}, status=405)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized - User not logged in"})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            backend_response = post_review(data) 
            
            print(f"--- Backend response received in add_review view: {backend_response}")

            if backend_response and not backend_response.get('error'):
                return JsonResponse({"status": 200, "message": "Review posted successfully", "data_from_backend": backend_response})
            else:
                error_message = backend_response.get('message', backend_response.get('details', 'Unknown error posting review to backend'))
                # Determine a more appropriate status code if possible from backend_response
                status_code_from_backend = backend_response.get('status_code', 400) if isinstance(backend_response, dict) else 400
                return JsonResponse({"status": status_code_from_backend, "message": f"Failed to post review: {error_message}"})

        except json.JSONDecodeError:
            return JsonResponse({"status": 400, "message": "Invalid JSON in request body"})
        except Exception as e:
            logger.error(f"Error in add_review view: {e}") # Make sure logger is defined
            return JsonResponse({"status": 500, "message": "Internal server error in add_review view"})
    else:
        return JsonResponse({"status": 405, "message": "Method not allowed"})
# ...
