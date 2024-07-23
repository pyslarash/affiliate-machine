from check_link import crawl

def crawl_multiple(starting_urls):
    for url in starting_urls:
        crawl([url])

if __name__ == "__main__":
    starting_urls_file = input("Enter the filename containing the list of starting URLs: ")
    with open(starting_urls_file, "r") as file:
        starting_urls = file.readlines()
        starting_urls = [url.strip() for url in starting_urls if url.strip()]  # Remove empty lines and strip whitespace
    crawl_multiple(starting_urls)