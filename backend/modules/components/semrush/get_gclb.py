import requests

def fetch_gclb_value(phpsessid, token):
    url = "https://suggestions.semrush.com/?q="  # Ensure the query parameter is correctly formatted if needed

    # Construct the headers with the dynamic PHPSESSID
    headers = {
        'Authorization': f'Bearer {token}',
        'Cookie': f'PHPSESSID={phpsessid}'
    }

    response = requests.get(url, headers=headers)

    # Check if the response status is OK
    if response.status_code == 200:
        # Extract the GCLB value from the Set-Cookie header
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        gclb_value = cookies.get('GCLB', 'GCLB cookie not found')

        # Print and return the GCLB value
        # print("GCLB Value:", gclb_value)
        return gclb_value
    else:
        print("Failed to retrieve GCLB Value, HTTP Status Code:", response.status_code)
        return None
