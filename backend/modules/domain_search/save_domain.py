# save_domain.py
import os

def save_domain(domain, filename):
    try:
        # Create the 'lists' directory if it doesn't exist
        if not os.path.exists("lists"):
            os.makedirs("lists")

        # Check if the file exists, if not, create it
        filepath = os.path.join("lists", f"{filename}.txt")
        if not os.path.isfile(filepath):
            open(filepath, 'a').close()

        # Save the domain into the file
        with open(filepath, "a") as file:
            file.write(domain + '\n')
        print(f"Domain '{domain}' saved successfully in '{filename}.txt'")
    except Exception as e:
        print(f"Error saving domain '{domain}': {e}")
