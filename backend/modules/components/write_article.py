from outline_json import outline_json
from components.sub_components.heading_calculator import heading_calculator
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

def write_article(min_words, max_words, min_headings, max_headings, min_paragraphs, post_title, directory_name):
    
    headings, subheadings = heading_calculator(min_headings, max_headings, products)