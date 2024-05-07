import requests
import json
from http.cookies import SimpleCookie

def semrush_login(email, password):
    url = "https://www.semrush.com/sso/authorize"
    payload = json.dumps({
        "locale": "en",
        "email": email,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    # print("Response Status Code:", response.status_code)
    # print("Response Headers:", response.headers)

    if response.status_code == 201:
        data = response.json()
        token = data.get('token', 'No token found')
        expires_at = data.get('expires_at', 'No expiry info')
        user_id = data.get('user_id', 'No user ID found')
        # print(f"Token: {token}, Expires at: {expires_at}, User ID: {user_id}")

        # Manually parse the Set-Cookie header to handle multiple cookies
        cookies_dict = {}
        for item in response.headers.get('Set-Cookie', '').split(','):
            if 'expires=' in item:
                continue
            parts = item.split(';')[0].split('=')
            if len(parts) == 2:
                cookies_dict[parts[0].strip()] = parts[1].strip()

        # print("Cookies from the response:", cookies_dict)

        # Extracting PHPSESSID
        phpsessid = cookies_dict.get('PHPSESSID', 'PHPSESSID not found')
        # print(f"PHPSESSID: {phpsessid}")

        return user_id, token, expires_at, phpsessid
    else:
        print("Failed to login")
        return None, None