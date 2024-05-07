import requests
import json

def fetch_api_key(phpsessid, token):
    url = "https://www.semrush.com/accounts/subscription-info/api/v1/header/"
    
    # Prepare the cookie in the required format
    headers = {
        'Authorization': f'Bearer {token}',
        'Cookie': f'PHPSESSID={phpsessid}'
    }

    # Make the GET request to fetch the API key
    response = requests.get(url, headers=headers)

    # Check the status code of the response to ensure the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the API key from the 'api_units' dictionary
        api_key = data.get('api_units', {}).get('api_key', 'No API Key Found')
        return api_key
    else:
        print(f"Failed to fetch API key, HTTP Status Code: {response.status_code}")
        return None