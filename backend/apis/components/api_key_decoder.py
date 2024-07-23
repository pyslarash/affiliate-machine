import os
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from database.models import UserEnv

load_dotenv()

# Retrieve or generate the encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
try:
    decoded_key = base64.urlsafe_b64decode(ENCRYPTION_KEY)
    cipher_suite = Fernet(decoded_key)
    print("Successfully initialized Fernet with the decoded key.")
except Exception as e:
    print(f"Failed to initialize Fernet with the key: {ENCRYPTION_KEY}, error: {e}")
    raise

def decrypt_api(api_key):
    try:
        decoded_api_key = base64.urlsafe_b64decode(api_key)
        decrypted_value = cipher_suite.decrypt(decoded_api_key).decode('utf-8')
        return decrypted_value
    except Exception as e:
        print(f"Error decrypting value, error: {e}")
        return None

def api_key_decoder(user_id, api_key_name):
    user_env = UserEnv.query.filter_by(user_id=user_id).first()
    if user_env:
        encrypted_api_key = getattr(user_env, api_key_name, None)
        if encrypted_api_key:
            display_value = decrypt_api(encrypted_api_key)
            if display_value:
                return display_value
            else:
                return "Failed to decrypt the API key."
        else:
            return f"{api_key_name} does not exist for the user."
    else:
        return "User environment not found."