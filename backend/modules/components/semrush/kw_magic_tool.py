import requests
import json

def fetch_keyword_ideas(phrase, user_id, api_key, auth, gclb_cookie, token):
    url = "https://www.semrush.com/kmtgw/rpc"

    payload = json.dumps({
        "id": 9,
        "jsonrpc": "2.0",
        "method": "ideas.GetKeywords",
        "params": {
            "mode": 0,
            "currency": "USD",
            "database": "us",
            "groups": [],
            "order": {"direction": 1, "field": "volume"},
            "page": {"number": 1, "size": 100},
            "phrase": phrase,
            "questions_only": False,
            "api_key": api_key,
            "user_id": user_id
        }
    })

    headers = {
        'Authorization': f'Bearer {token}',
        'authorization': auth,
        'Content-Type': 'application/json',
        'Cookie': gclb_cookie
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json()

def main():
    # Collect necessary inputs from the user
    print("Please enter the required information to fetch keyword ideas.")
    phrase = input("Enter the focus keyword: ")
    user_id = input("Enter your user ID: ")
    api_key = input("Enter your API key: ")
    auth = input("Enter the authorization token: ")
    gclb_cookie = input("Enter the GCLB cookie value: ")

    # Fetch keyword ideas using the provided data
    keyword_ideas = fetch_keyword_ideas(phrase, user_id, api_key, auth, gclb_cookie)

    # Print the results
    print("Keyword Ideas Response:")
    print(json.dumps(keyword_ideas, indent=4))  # Pretty print the JSON response

if __name__ == "__main__":
    main()