import requests
import os
import time
import csv
import pandas as pd
from dotenv import load_dotenv
import cgi

load_dotenv()

api_key = os.getenv("MYADDR_API_KEY")

def upload_file(file_name):
    url = f"https://seo-rank.my-addr.com/upload_file_ahrefs.php?secret={api_key}&filename={file_name}"

    file_path = f"myaddr/{file_name}.txt"

    with open(file_path, 'rb') as file:
        files = {'mainfile': (file_name + '.txt', file, 'text/plain')}
        response = requests.post(url, files=files)

    return response.text.strip()  # Strip whitespace from the response

def check_file_status(file_id):
    url = f"https://seo-rank.my-addr.com/file_info.php?secret={api_key}&id={file_id}"
    
    # Check the status of the file every 2 minutes
    while True:
        response = requests.get(url)
        file_info = response.text.strip()  # Strip whitespace from the response
        print("File status:", file_info)
        if "progress" in file_info or "waiting" in file_info:
            print("File is still in progress or waiting. Checking again in 2 minutes...")
            time.sleep(120)  # Wait for 2 minutes before checking again
        elif "finished" in file_info:
            print("File processing finished.")
            info_parts = file_info.split('|')
            if len(info_parts) > 6:
                csv_url = info_parts[-2].strip()  # Extract the second-to-last URL
                return csv_url
        else:
            print("Unknown status. Exiting.")
            return None

def parse_csv_to_json(csv_url):
    response = requests.get(csv_url)
    csv_file_name = "data.csv"  # Set a default filename
    
    if "content-disposition" in response.headers:
        content_disp_header = response.headers["content-disposition"]
        _, params = cgi.parse_header(content_disp_header)
        if "filename" in params:
            csv_file_name = params["filename"]
    
    csv_file_path = f"myaddr/csv/{csv_file_name}"
    
    # Save CSV file
    with open(csv_file_path, 'wb') as csv_file:  # Open in binary mode
        csv_file.write(response.content)

    # Read CSV into DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records', indent=4)
    
    return json_data


def main():
    file_name = input("Enter the filename (without extension) to upload: ")
    file_id = upload_file(file_name)
    print(f"File uploaded. ID: {file_id}")

    # Wait for 30 seconds before starting to check the status
    print("Waiting for 30 seconds before checking the status...")
    time.sleep(30)

    # Check the file status
    csv_url = check_file_status(file_id)
    if csv_url is not None:
        print("Downloading CSV from:", csv_url)
        json_data = parse_csv_to_json(csv_url)
        print("JSON Data:")
        print(json_data)

if __name__ == "__main__":
    main()
