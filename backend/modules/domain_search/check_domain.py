import whois
from urllib.parse import urlparse

def check_domain_availability(domain_name):
    try:
        parsed_url = urlparse(domain_name)
        if parsed_url.scheme:  # Ignore URLs with scheme (e.g., http://example.com)
            return False
        domain = parsed_url.netloc.split('.')[-1]  # Extract TLD
        if domain.lower() == 'com':
            data = whois.whois(domain_name)
            if isinstance(data, str):
                return True
            else:
                return False
        else:
            print("Only .com domains are supported.")
            return False
    except Exception as e:
        print(f"Error checking domain availability: {e}")
        return False

if __name__ == "__main__":
    domain = input("Enter domain name: ")
    availability = check_domain_availability(domain)
    print(availability)
