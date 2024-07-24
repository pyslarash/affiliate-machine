import os
import requests
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv
import whoisdomain as whois
from flask import jsonify, request
import traceback
import json

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')

def domain_whois_check(domain_name):
    try:
        domain_info = whois.query(domain_name)
        print(domain_info)
        if domain_info == None:
            return jsonify({'status': 'available', 'domain': domain_name}), 200
        
        expiration_datetime = domain_info.expiration_date
        if isinstance(expiration_datetime, list):
            expiration_datetime = expiration_datetime[0]
            
        creation_datetime = domain_info.creation_date
        if isinstance(creation_datetime, list):
            creation_datetime = creation_datetime[0]
            
        updated_datetime = domain_info.last_updated
        if isinstance(updated_datetime, list):
            updated_datetime = updated_datetime[0]
            
        name_servers = domain_info.name_servers
        if not isinstance(name_servers, list):
            name_servers = [name_servers]
            
        name_servers = [ns.rstrip('.') for ns in name_servers]
            
        domain_record = {
            'domain': domain_name,
            'expiration_date': expiration_datetime.strftime('%Y-%m-%d') if expiration_datetime else None,
            'expiration_time': expiration_datetime.strftime('%H:%M:%S') if expiration_datetime else None,
            'creation_date': creation_datetime.strftime('%Y-%m-%d') if creation_datetime else None,
            'creation_time': creation_datetime.strftime('%H:%M:%S') if creation_datetime else None,
            'updated_date': updated_datetime.strftime('%Y-%m-%d') if updated_datetime else None,
            'updated_time': updated_datetime.strftime('%H:%M:%S') if updated_datetime else None,
            'name_servers': name_servers if name_servers else None
        }
        
        if domain_record['expiration_date']:
            return jsonify({'domain': domain_record, 'status': 'unavailable'}), 200
        else:
            return jsonify({'error': 'Expiration date not found for the domain.'}), 404
    except Exception as e:
        return jsonify({'error': f'Error fetching WHOIS data for domain {domain_name}: {str(e)}', 'traceback': traceback.format_exc()}), 500
    
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
        return {"error": response.text, "status_code": response.status_code, 'traceback': traceback.format_exc()}
    
def check_domdetailer_domain(domain_name):
    api_key = domdetailer_api()
    # Define the URL with the provided domain name and API key
    domain_url = f"http://domdetailer.com/api/checkDomain.php?domain={domain_name}&app=DomDetailer&apikey={api_key}&majesticChoice=root"
    
    # Make the GET request to the checkDomain endpoint
    response = requests.get(domain_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Handle errors by returning the response text and status code
        return {"error": response.text, "status_code": response.status_code, 'traceback': traceback.format_exc()}