import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instantiate the OpenAI client
client = OpenAI()

def list_openai_assistants():
    my_assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    print("My assistants:")
    assistant_names = []
    for assistant in my_assistants.data:
        if hasattr(assistant, 'name') and assistant.name:
            assistant_names.append(assistant.name)
    assistant_names.sort()
    for name in assistant_names:
        print(name)
    
def main():
    print("What would you like to do?")
    print("1. List my OpenAI Assistants")
    
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        list_openai_assistants()
    else:
        print("Invalid choice. Please enter a valid number.")
    
if __name__ == "__main__":
    main()