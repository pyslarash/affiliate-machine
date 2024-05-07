import requests
from newspaper import Article
from urllib.parse import urlparse, urljoin
from requests.exceptions import RequestException
from check_domain import check_domain_availability
from save_domain import save_domain
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import html

checked_domains = set()

def get_links(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}  # Random User-Agent header
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True, verify=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        article = Article(url)
        article.download()
        article.parse()
        html_content = html.unescape(article.html)  # Decode HTML entities
        soup = BeautifulSoup(html_content, 'html.parser')
        base_url = urlparse(url)
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if not href.startswith(('http://', 'https://')):  # Handle relative URLs
                href = urljoin(url, href)
            parsed_href = urlparse(href)
            if parsed_href.scheme and parsed_href.netloc:  # Check if valid absolute URL
                links.append(href)
        # Filter out URLs with fragments
        links = [link for link in links if not urlparse(link).fragment]
        return links
    except Exception as e:
        print(f"Error getting links from {url}: {e}")
        return []

def get_external_links(url):
    try:
        links = get_links(url)
        parsed_url = urlparse(url)
        base_domain = parsed_url.netloc
        external_links = [urljoin(url, link) for link in links if urlparse(link).netloc != base_domain]
        return external_links
    except Exception as e:
        print(f"Error getting external links from {url}: {e}")
        return []

def check_links(links):
    for link in links:
        domain = urlparse(link).netloc
        if domain not in checked_domains:
            checked_domains.add(domain)
            try:
                response = requests.head(link, timeout=10, allow_redirects=True, verify=True)
                response.raise_for_status()  # Raise an exception for HTTP errors
                if response.status_code == 200:
                    print(f"External link {link} is alive.")
                else:
                    print(f"External link {link} is dead.")
                    # Check domain availability
                    domain_availability = check_domain_availability(domain)
                    if domain_availability:
                        print(f"Domain {domain} is available.")
                        save_domain(domain, "available_domains")  # Save the available domain
                    else:
                        print(f"Domain {domain} is not available.")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    print(f"Received 403 Forbidden response for {link}. Skipping...")
                else:
                    print(f"Error checking external link {link}: {e}")
            except RequestException as e:
                print(f"Error checking external link {link}: {e}")

def crawl(urls, visited=None):
    if visited is None:
        visited = set()
    for url in urls:
        if url not in visited:
            visited.add(url)
            print(f"Crawling {url}")
            external_links = get_external_links(url)
            check_links(external_links)
            internal_links = [link for link in get_links(url) if link not in external_links]
            internal_links = [link for link in internal_links if not urlparse(link).fragment]  # Filter out URLs with fragments
            for link in internal_links:
                crawl([link], visited)  # Recursively crawl internal links

if __name__ == "__main__":
    filename = input("Enter the filename containing the list of starting URLs: ")
    with open(filename, 'r') as file:
        starting_urls = [line.strip() for line in file.readlines()]
    crawl(starting_urls)
