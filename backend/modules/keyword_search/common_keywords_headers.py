import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk import pos_tag
from collections import defaultdict

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def get_headers_text_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        headers_text = ' '.join([header.get_text() for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        return headers_text
    except requests.RequestException as e:
        print(f"Failed to fetch webpage: {url} with error {e}")
        return ""

def extract_nouns_and_noun_phrases(text):
    tokenizer = RegexpTokenizer(r'\w+')  # Removes punctuation
    words = tokenizer.tokenize(text.lower())  # Lowercase text
    tagged_words = pos_tag(words)
    nouns = [word for word, tag in tagged_words if tag.startswith('NN')]  # Filter nouns

    nouns = [noun for noun in nouns if len(noun) > 1]  # Filter out single characters

    bigrams = [' '.join(bigram) for bigram in nltk.bigrams(nouns) if all(len(word) > 1 for word in bigram)]
    trigrams = [' '.join(trigram) for trigram in nltk.trigrams(nouns) if all(len(word) > 1 for word in trigram)]

    return set(nouns + bigrams + trigrams)

def find_common_noun_phrases(urls):
    all_noun_phrases = []
    for url in urls:
        text = get_headers_text_from_url(url)
        noun_phrases = extract_nouns_and_noun_phrases(text)
        all_noun_phrases.append(noun_phrases)
    
    common_noun_phrases = set.intersection(*all_noun_phrases)
    return common_noun_phrases

def noun_phrase_stats(urls, common_noun_phrases):
    noun_phrase_counts = {url: defaultdict(int) for url in urls}
    for url in urls:
        text = get_headers_text_from_url(url).lower()
        for phrase in common_noun_phrases:
            noun_phrase_counts[url][phrase] = text.count(phrase)
    
    return noun_phrase_counts

def main():
    urls = [
        "https://www.convinceandconvert.com/digital-marketing/expert-tips-best-seo-strategies/",
        "https://www.webfx.com/blog/seo/seo-marketing-strategy/",
        "https://seo-hacker.com/daring-seo-strategies-2018/",
    ]
    
    common_noun_phrases = find_common_noun_phrases(urls)
    print("Common Noun Phrases in Headers:", common_noun_phrases)
    
    stats = noun_phrase_stats(urls, common_noun_phrases)
    for phrase in common_noun_phrases:
        min_count = min(stats[url][phrase] for url in urls)
        max_count = max(stats[url][phrase] for url in urls)
        print(f"Noun Phrase '{phrase}' occurs from {min_count} to {max_count} times across the webpage headers.")

if __name__ == "__main__":
    main()
