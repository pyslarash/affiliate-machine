import os
import requests
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv
from flask import jsonify, request
import json

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')

@jwt_required()
def domdetailer_api():
    # Extract the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header:
        jwt_token = auth_header.split(" ")[1]  # Extract the token part
    else:
        return jsonify({"msg": "Missing Authorization Header"}), 401
    
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.get(f"{BACKEND_URL}/get_domdetailer_api_key", headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        domdetailer_api_key = response_json.get('domdetailer_api_key')
        return domdetailer_api_key
    else:
        return response.text, response.status_code

def check_domdetailer_balance():
    api_key = domdetailer_api()
    # Define the URL with the provided API key
    balance_url = f"http://domdetailer.com/api/checkBalance.php?apikey={api_key}&app=DomDetailer"
    
    # Make the GET request to the checkBalance endpoint
    response = requests.get(balance_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        balance_data = response.json()
        # Extract the number of units left from the response
        units_left = balance_data[1]  # Assuming balance_data is a list and units left is at index 1
        return {"units_left": int(units_left)}
    else:
        # Handle errors by returning the response text and status code
        return {"error": response.text, "status_code": response.status_code}
    
def check_domdetailer_domain(domain_name):
    api_key = domdetailer_api()
    # Define the URL with the provided domain name and API key
    domain_url = f"http://domdetailer.com/api/checkDomain.php?domain={domain_name}&app=DomDetailer&apikey={api_key}&majesticChoice=root"
    
    # Make the GET request to the checkDomain endpoint
    response = requests.get(domain_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        domain_data = response.json()
        # Return the formatted JSON
        return json.dumps(domain_data, indent=2)
    else:
        # Handle errors by returning the response text and status code
        return json.dumps({"error": response.text, "status_code": response.status_code}, indent=2)