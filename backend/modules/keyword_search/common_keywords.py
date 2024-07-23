import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk import pos_tag
from collections import defaultdict

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def get_text_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        visible_text = ' '.join(soup.stripped_strings)
        return visible_text
    except requests.RequestException as e:
        print(f"Failed to fetch webpage: {url} with error {e}")
        return ""

def extract_nouns_and_noun_phrases(text):
    tokenizer = RegexpTokenizer(r'\w+')  # Tokenizer that removes punctuation
    words = tokenizer.tokenize(text.lower())
    words = [word.lower() for word in words if word.isalpha()]  # Filter non-alphabetic tokens
    tagged_words = pos_tag(words)
    nouns = [word for word, tag in tagged_words if tag.startswith('NN')]  # Select only nouns

    # Filter out any remaining single character 'words' which might be errors or stray punctuation
    nouns = [noun for noun in nouns if len(noun) > 1]

    # Create bigrams and trigrams from nouns only
    bigrams = [' '.join(bigram) for bigram in nltk.bigrams(nouns) if all(len(word) > 1 for word in bigram)]
    trigrams = [' '.join(trigram) for trigram in nltk.trigrams(nouns) if all(len(word) > 1 for word in trigram)]

    # Combine single nouns, bigrams, and trigrams into one set
    noun_phrases = set(nouns + bigrams + trigrams)
    return noun_phrases

def find_common_noun_phrases(urls):
    all_noun_phrases = []
    for url in urls:
        text = get_text_from_url(url)
        noun_phrases = extract_nouns_and_noun_phrases(text)
        all_noun_phrases.append(noun_phrases)
    
    common_noun_phrases = set.intersection(*all_noun_phrases)
    return common_noun_phrases

def noun_phrase_stats(urls, common_noun_phrases):
    noun_phrase_counts = {url: defaultdict(int) for url in urls}
    for url in urls:
        text = get_text_from_url(url).lower()
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
    print("Common Noun Phrases:", common_noun_phrases)
    
    stats = noun_phrase_stats(urls, common_noun_phrases)
    for phrase in common_noun_phrases:
        min_count = min(stats[url][phrase] for url in urls)
        max_count = max(stats[url][phrase] for url in urls)
        print(f"Noun Phrase '{phrase}' occurs from {min_count} to {max_count} times across the webpages.")

if __name__ == "__main__":
    main()
