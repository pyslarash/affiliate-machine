import os
from pyczds.client import CZDSClient
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import UserEnv
from apis.api_keys import decrypt_value
from flask import jsonify
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
from datetime import datetime, timedelta
import gzip
import re

load_dotenv()

szds_dir = os.getenv('CZDS_DIR')

@jwt_required()
def get_czds_credentials():
    try:
        current_user_id = get_jwt_identity()
        
        user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
        if user_env and user_env.czds_login and user_env.czds_password:
            return {
                "czds_login": decrypt_value(user_env.czds_login),
                "czds_password": decrypt_value(user_env.czds_password)
            }, 200
        else:
            return {
                "error": "CZDS credentials not found for the current user"
            }, 404
    
    except Exception as e:
        return {
            "error": str(e)
        }, 500

@jwt_required()
def get_czds_cred():
    try:
        credentials, status_code = get_czds_credentials()
        
        if status_code == 200:
            czds_login = credentials['czds_login']
            czds_password = credentials['czds_password']
            
            client = CZDSClient(czds_login, czds_password)
            return client
        
        else:
            raise Exception(f"Failed to retrieve CZDS credentials: {credentials.get('error', 'Unknown error')}")
    
    except Exception as e:
        raise Exception(f"Error retrieving CZDS credentials: {str(e)}")

@jwt_required()
def get_czds_zonefiles_list():
    try:
        client = get_czds_cred()
        
        zonefile_urls = client.get_zonefiles_list()
        
        zonefiles_json = {'zonefiles': zonefile_urls}
        return zonefiles_json, 200
    
    except Exception as e:
        print(f"Error fetching zonefiles: {str(e)}")
        return {'error': 'Error fetching zonefiles'}, 500

@jwt_required()
def get_czds_zonefiles_heads(zone):    
    try:
        client = get_czds_cred()
        
        zonefile_urls = client.get_zonefiles_list()
        zonefile_url = next((url for url in zonefile_urls if f"{zone}.zone" in url), None)
        
        if zonefile_url:
            zonefile_heads = client.head_zonefile(zonefile_url)
            
            def convert_to_dict(obj):
                if isinstance(obj, CaseInsensitiveDict):
                    return {key: convert_to_dict(value) for key, value in obj.items()}
                elif isinstance(obj, dict):
                    return {key: convert_to_dict(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_to_dict(item) for item in obj]
                else:
                    return obj
            
            zonefile_heads_dict = convert_to_dict(zonefile_heads)
            
            return jsonify(zonefile_heads_dict), 200
        else:
            return jsonify({'error': 'Zone file not found'}), 404
    
    except Exception as e:
        return jsonify({'error': 'Error fetching zonefile heads'}), 500

@jwt_required()
def download_czds_zonefile(zone):
    try:
        client = get_czds_cred()
        
        zonefile_urls = client.get_zonefiles_list()
        zonefile_url = next((url for url in zonefile_urls if f"{zone}.zone" in url), None)
        zone_filename = f'{zone}_zonefile.gz'
        
        # Define the download directory
        download_dir = f"modules/czds/{szds_dir}/"
        
        # Check if the directory exists, if not, create it
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        file_path = os.path.join(download_dir, zone_filename)
        print(f"Filepath: {file_path}")
        
        # Check if the file exists and if it was modified within the last 24 hours
        if os.path.exists(file_path):
            last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if datetime.now() - last_modified_time < timedelta(hours=24):
                return jsonify({'error': 'Zone file was downloaded less than 24 hours ago'}), 403
        
        # Download the zonefile
        client.get_zonefile(zonefile_url, download_dir=download_dir, filename=zone_filename)
        return jsonify({'message': f'Zone file was saved to {file_path}'}), 200
    
    except Exception as e:
        print(f"Error fetching zonefiles: {str(e)}")
        return jsonify({'error': 'Error downloading zonefile'}), 500

@jwt_required()   
def display_zonefile_contents(zone):
    file_path = f"modules/czds/{szds_dir}/{zone}_zonefile.gz"
    
    try:
        extracted_content = set()
        
        with gzip.open(file_path, 'rt') as f:
            for line in f:
                # Extract the domain names
                parts = line.split()
                if len(parts) > 0:
                    domain_name = parts[0].rstrip('.')
                    # Match second-level domains
                    match = re.match(r'^(?:[a-z0-9-]+\.)*([a-z0-9-]+\.[a-z]+)$', domain_name)
                    if match:
                        extracted_content.add(match.group(1))
        
        return jsonify({'domains': list(extracted_content)}), 200
    
    except Exception as e:
        print(f"Error displaying zonefile contents: {str(e)}")
        return jsonify({'error': 'Error reading zonefile'}), 500
    
