import requests
import json

def fetch_token(api_key, user_id, phpsessid, token):
    url = "https://www.semrush.com/kmtgw/rpc"
    
    # Construct the payload using function parameters
    payload_dict = {
        "id": 5,
        "jsonrpc": "2.0",
        "method": "tokens.GetIdeas",
        "params": {
            "mode": 0,
            "currency": "USD",
            "database": "us",
            "filter": {
                "phrase": [],
                "competition_level": [],
                "cpc": [],
                "difficulty": [],
                "results": [],
                "serp_features": [{"inverted": False, "value": []}],
                "volume": [],
                "words_count": [],
                "phrase_include_logic": 0
            },
            "groups": [],
            "order": {
                "direction": 1,
                "field": "volume"
            },
            "phrase": " ",
            "questions_only": False,
            "api_key": api_key,
            "user_id": user_id
        }
    }

    # Convert the dictionary to a JSON string
    payload = json.dumps(payload_dict)

    # Set headers including the PHPSESSID
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',  # Correct content type
        'Cookie': f'PHPSESSID={phpsessid}'  # Only include PHPSESSID cookie
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        # Attempt to extract the token from the response
        token = response_data.get('result', {}).get('token', None)
        if token:
            return token
        else:
            print("Token not found in response")
            return None
    else:
        print(f"Failed to fetch token, HTTP Status Code: {response.status_code}")
        return None