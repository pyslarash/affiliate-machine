import requests
from bs4 import BeautifulSoup
import re

def count_keyword_occurrences(url, keyword):
    """
    Counts the occurrences of a keyword on a webpage.
    
    Args:
        url (str): The URL of the webpage.
        keyword (str): The keyword to search for.

    Returns:
        int: The number of occurrences of the keyword on the webpage.
    """
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Make a request to the URL
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Will raise HTTPError for bad requests (400 or 500)
    except requests.RequestException as e:
        print(f"Failed to fetch webpage: {url} with error {e}")
        return 0

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all visible text on the webpage
    visible_text = ' '.join(soup.stripped_strings)
    
    # Count occurrences of the keyword in the visible text using regex for whole word match
    pattern = rf'\b{re.escape(keyword)}\b'
    occurrences = len(re.findall(pattern, visible_text, re.IGNORECASE))
    
    return occurrences



def main():
    # URL of the webpage to check
    url = "https://medium.com/@michael.slashventures/unlocking-success-best-seo-strategies-and-best-practices-fab77b3e6f0f"
    
    # Keyword to search for
    keyword = "best seo strategies"
    
    # Count occurrences of the keyword on the webpage
    occurrences = count_keyword_occurrences(url, keyword)
    
    print(f"Keyword '{keyword}' occurs {occurrences} times on the webpage.")

if __name__ == "__main__":
    main()
