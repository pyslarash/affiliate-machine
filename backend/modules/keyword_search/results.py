import os
import requests
import newspaper
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from dotenv import load_dotenv
import re
from fake_useragent import UserAgent

# Load environment variables from .env file
load_dotenv()

# Load environment variables
api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
cx = os.getenv("GOOGLE_CX")

def extract_domain_name(url):
    """
    Extracts the domain name from the given URL.
    
    Args:
        url (str): The URL from which to extract the domain name.
    
    Returns:
        str: The domain name extracted from the URL.
    """
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain

def extract_links(url):
    """
    Extracts all internal and external links from the given URL.
    
    Args:
        url (str): The URL from which to extract links.
    
    Returns:
        tuple: A tuple containing two integers - total number of internal links and total number of external links.
    """
    internal_links_count = 0
    external_links_count = 0
    
    # Make a request to the URL with fake user agent
    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        base_url = url
        
        # Extract all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            domain_name = extract_domain_name(absolute_url)
            
            # Check if the link is internal or external
            if domain_name == extract_domain_name(url):
                internal_links_count += 1
            else:
                external_links_count += 1
    
    return internal_links_count, external_links_count

def extract_article_info(url):
    """
    Extracts various information about the article content from the given URL.
    
    Args:
        url (str): The URL of the article.
    
    Returns:
        dict: A dictionary containing information about the article content.
            It contains keys: "word_count", "num_paragraphs", "num_headers", "num_images", "num_links".
    """
    # Make a request to the URL with fake user agent
    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Calculate word count
        word_count = len(soup.get_text().split())
        
        # Calculate number of paragraphs
        num_paragraphs = len(soup.find_all('p'))
        
        # Calculate number of headers (h1, h2, h3, etc.)
        headers = [tag.name for tag in soup.find_all(re.compile(r'^h\d$'))]
        num_headers = {f"h{i}": headers.count(f"h{i}") for i in range(1, 7)}
        
        # Calculate number of images
        num_images = len(soup.find_all('img'))
        
        # Calculate number of links
        num_links = len(soup.find_all('a'))
        
        return {
            "word_count": word_count,
            "num_paragraphs": num_paragraphs,
            "num_headers": num_headers,
            "num_images": num_images,
            "num_links": num_links
        }
    else:
        return None

def fetch_search_results(api_key, cx, keyword, num_results=10):
    """
    Fetches search results for a given keyword using the Google Custom Search API.
    
    Args:
        api_key (str): Google Custom Search API key.
        cx (str): Custom search engine ID (cx).
        keyword (str): The keyword to search for.
        num_results (int): Number of search results to retrieve. Defaults to 10.
    
    Returns:
        dict: A dictionary containing information about the search request.
            It contains keys: "total_results", "results", "statistics".
            "total_results" provides the total number of search results.
            "results" is a list of dictionaries, each containing information about a search result.
            Each dictionary contains keys: "title", "snippet", "link", "domain_name", "article_info", "internal_links_count", "external_links_count".
            "article_info" contains various information about the article content.
            "internal_links_count" provides the total number of internal links found on the page.
            "external_links_count" provides the total number of external links found on the page.
            "statistics" contains statistics across all search results, including minimum and maximum values.
    """
    results = []
    word_counts = []
    num_paragraphs_list = []
    num_headers_list = {f"h{i}": [] for i in range(1, 7)}
    num_images_list = []
    num_links_list = []
    internal_links_count_total = 0
    external_links_count_total = 0
    min_internal_links = float('inf')
    max_internal_links = float('-inf')
    min_external_links = float('inf')
    max_external_links = float('-inf')
    
    # Make a request to the Google Custom Search API
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q=\"{keyword}\"&num={num_results}"
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if response.status_code == 200:
        # Extract information from the search request
        total_results = int(data["queries"]["request"][0]["totalResults"])
        
        # Extract information from each search result
        for item in data.get("items", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            domain_name = extract_domain_name(link)
            
            # Extract article info
            article_info = extract_article_info(link)
            
            if article_info is not None:  # Check if article info is available
                # Extract internal and external links
                internal_links_count, external_links_count = extract_links(link)
                
                # Update statistics
                word_counts.append(article_info["word_count"])
                num_paragraphs_list.append(article_info["num_paragraphs"])
                num_images_list.append(article_info["num_images"])
                num_links_list.append(article_info["num_links"])
                for header, count in article_info["num_headers"].items():
                    num_headers_list[header].append(count)
                
                # Update total counts
                internal_links_count_total += internal_links_count
                external_links_count_total += external_links_count
                
                # Update min/max internal/external link counts
                min_internal_links = min(min_internal_links, internal_links_count)
                max_internal_links = max(max_internal_links, internal_links_count)
                min_external_links = min(min_external_links, external_links_count)
                max_external_links = max(max_external_links, external_links_count)
                
                result_info = {
                    "title": title,
                    "snippet": snippet,
                    "link": link,
                    "domain_name": domain_name,
                    "article_info": article_info,
                    "internal_links_count": internal_links_count,
                    "external_links_count": external_links_count
                }
                results.append(result_info)
            else:
                print(f"Skipping result due to unavailable article info: {link}")
        
        # Calculate statistics across all search results
        statistics = {
            "min_word_count": min(word_counts),
            "max_word_count": max(word_counts),
            "min_num_paragraphs": min(num_paragraphs_list),
            "max_num_paragraphs": max(num_paragraphs_list),
            "min_num_headers": {header: min(counts) for header, counts in num_headers_list.items()},
            "max_num_headers": {header: max(counts) for header, counts in num_headers_list.items()},
            "min_num_images": min(num_images_list),
            "max_num_images": max(num_images_list),
            "min_num_links": min(num_links_list),
            "max_num_links": max(num_links_list),
            "min_internal_links": min_internal_links,
            "max_internal_links": max_internal_links,
            "min_external_links": min_external_links,
            "max_external_links": max_external_links
        }
        
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        statistics = {}
    
    return {"total_results": total_results, "results": results, "statistics": statistics}

def main():
    # Get keyword from user input
    keyword = input("Enter the keyword to search for: ")
    
    # Fetch search results
    search_data = fetch_search_results(api_key, cx, keyword)
    
    # Print search results
    print(f"Total Results: {search_data['total_results']}")
    print("--------------------")
    for result in search_data['results']:
        print(f"Title: {result['title']}")
        print(f"Snippet: {result['snippet']}")
        print(f"Link: {result['link']}")
        print(f"Domain Name: {result['domain_name']}")
        print(f"Article Info: {result['article_info']}")
        print(f"Internal Links Count: {result['internal_links_count']}")
        print(f"External Links Count: {result['external_links_count']}")
        print("--------------------")

    # Display statistics
    statistics = search_data['statistics']
    print("Statistics Across All Search Results:")
    print(f"Minimum Word Count: {statistics['min_word_count']}")
    print(f"Maximum Word Count: {statistics['max_word_count']}")
    print(f"Minimum Number of Paragraphs: {statistics['min_num_paragraphs']}")
    print(f"Maximum Number of Paragraphs: {statistics['max_num_paragraphs']}")
    print(f"Minimum Number of Images: {statistics['min_num_images']}")
    print(f"Maximum Number of Images: {statistics['max_num_images']}")
    print(f"Minimum Number of Links: {statistics['min_num_links']}")
    print(f"Maximum Number of Links: {statistics['max_num_links']}")
    print(f"Minimum Number of Internal Links: {statistics['min_internal_links']}")
    print(f"Maximum Number of Internal Links: {statistics['max_internal_links']}")
    print(f"Minimum Number of External Links: {statistics['min_external_links']}")
    print(f"Maximum Number of External Links: {statistics['max_external_links']}")
    print("Minimum Number of Headers:")
    for header, count in statistics['min_num_headers'].items():
        print(f"  {header}: {count}")
    print("Maximum Number of Headers:")
    for header, count in statistics['max_num_headers'].items():
        print(f"  {header}: {count}")

if __name__ == "__main__":
    main()
