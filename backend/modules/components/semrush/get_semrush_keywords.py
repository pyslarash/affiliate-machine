from sem_login import semrush_login
from get_api_key import fetch_api_key
from get_gclb import fetch_gclb_value
from get_auth import fetch_token
from kw_magic_tool import fetch_keyword_ideas

def get_keyword_ideas(email, password, keyword):
    # Log in and get user_id and phpsessid
    user_id, token, expires_at, phpsessid = semrush_login(email, password)
    print(f"User ID: {user_id}; PHPSESSID: {phpsessid}")
    if not user_id or not phpsessid:
        return "Login failed. Please check your credentials."

    # Fetch API key using phpsessid
    api_key = fetch_api_key(phpsessid, token)
    print(f"API Key: {api_key}")
    if not api_key:
        return "Failed to retrieve API Key."

    # Fetch GCLB cookie value
    gclb = fetch_gclb_value(phpsessid, token)
    print(f"GCLB: {gclb}")
    if not gclb:
        return "Failed to retrieve GCLB value."

    # Fetch authorization token using api_key, user_id, and phpsessid
    auth = fetch_token(api_key, user_id, phpsessid, token)
    print(f"Auth: {auth}")
    if not auth:
        return "Failed to authenticate."

    # Fetch keyword ideas using all gathered data
    keyword_ideas = fetch_keyword_ideas(keyword, user_id, api_key, auth, gclb, token)
    return keyword_ideas

def main():
    # Ask the user for their email, password, and focus keyword
    email = input("Enter your SEMrush email: ")
    password = input("Enter your SEMrush password: ")
    keyword = input("Enter your focus keyword for SEO ideas: ")

    # Get keyword ideas and print them
    keyword_ideas = get_keyword_ideas(email, password, keyword)
    print("Keyword Ideas:", keyword_ideas)

if __name__ == "__main__":
    main()
