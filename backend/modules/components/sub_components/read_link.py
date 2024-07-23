from newspaper import Article
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()
summarizer_id = os.getenv("SUMMARIZER_ID")

def extract_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title, article.text
    except Exception as e:
        return f"Error: {e}"

def get_article(url):
    try:
        title, article_text = extract_article(url)
        return title, article_text
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None, None

def get_summary(url):
    title, article_text = extract_article(url)
    summarizer_assistant = client.beta.assistants.retrieve(summarizer_id)
    summarizer_thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                    Write a summary for an article named {title}.
                    This is the full text of that article: {article_text}
                """
            }
        ]
    )
    run = client.beta.threads.runs.create(
        thread_id=summarizer_thread.id,
        assistant_id=summarizer_assistant.id
    )

    # Poll the status of the run until it's completed, failed, or cancelled
    while run.status not in ["completed", "failed", "cancelled"]:
        time.sleep(1)  # Wait for 1 second before polling again
        run = client.beta.threads.runs.retrieve(thread_id=summarizer_thread.id, run_id=run.id)

    if run.status == "completed":
        # Fetch the messages added by the Assistant to the thread
        messages = client.beta.threads.messages.list(thread_id=summarizer_thread.id)
        summary = None
        for msg in messages:
            if msg.role == "assistant":
                content_type = msg.content[0].type if msg.content else None
                if content_type == "text":
                    summary = msg.content[0].text.value if msg.content[0].text else None
                    break
        
        if summary:
            return title, summary
        else:
            print("No summary found in the response.")
    elif run.status == "failed":
        print("Run failed. Please check the last_error field in the Run object for details.")
    else:  # run.status == "cancelled"
        print("Run was cancelled.")
    return None, None

def main():
    try:
        # Ask the user to input the article link
        url = input("Please insert the article link: ")
        
        # Get the article text and title
        title, article_text = get_summary(url)
        
        # Print the title and article text
        if title and article_text:
            print(f"Title: {title}")
            print(f"\nSummary:\n{article_text}")
        else:
            print("Failed to retrieve article.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()