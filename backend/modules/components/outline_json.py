import os
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()

article_writer_id = os.getenv("ARTICLE_WRITER_ID")

article_writer = client.beta.assistants.retrieve(article_writer_id)

def outline_json(keyword, topic):
    summarizer_thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                    Write an outline for a blog post for this topic: {topic}.
                    This is your focus keyword: {keyword}
                    Only include the "body" with hedings, subheadings, and summary.
                """
            }
        ]
    )
    run = client.beta.threads.runs.create(
        thread_id=summarizer_thread.id,
        assistant_id=article_writer.id,
        response_format={"type": "json_object"}
    )
    
    # Poll the status of the run until it's completed, failed, or cancelled
    while run.status not in ["completed", "failed", "cancelled"]:
        time.sleep(1)  # Wait for 1 second before polling again
        run = client.beta.threads.runs.retrieve(thread_id=summarizer_thread.id, run_id=run.id)

    if run.status == "completed":
        # Fetch the messages added by the Assistant to the thread
        messages = client.beta.threads.messages.list(thread_id=summarizer_thread.id)
        outline_json = None
        for msg in messages:
            if msg.role == "assistant":
                content_type = msg.content[0].type if msg.content else None
                if content_type == "text":
                    outline_json = msg.content[0].text.value if msg.content[0].text else None
                    break
        
        if outline_json:
            return outline_json
        else:
            print("No JSON found in the response.")
    elif run.status == "failed":
        print("Run failed. Please check the last_error field in the Run object for details.")
    else:  # run.status == "cancelled"
        print("Run was cancelled.")
    return None