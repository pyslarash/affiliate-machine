import json
from database.models import UserEnv
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import base64

load_dotenv()

# Function to update .env file
def set_key_in_env(key):
    env_file_path = '.env'
    if not os.path.exists(env_file_path):
        with open(env_file_path, 'w') as env_file:
            env_file.write(f'ENCRYPTION_KEY={key}\n')
    else:
        with open(env_file_path, 'r') as env_file:
            lines = env_file.readlines()

        with open(env_file_path, 'w') as env_file:
            key_written = False
            for line in lines:
                if line.startswith('ENCRYPTION_KEY'):
                    env_file.write(f'ENCRYPTION_KEY={key}\n')
                    key_written = True
                else:
                    env_file.write(line)
            if not key_written:
                env_file.write(f'ENCRYPTION_KEY={key}\n')

# Retrieve or generate the encryption key
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# If the encryption key is not present in the environment variables, generate a new one
if ENCRYPTION_KEY is None:
    # Generate a new encryption key
    new_key = Fernet.generate_key()
    # Encode the key to base64 before storing it in the environment variable
    ENCRYPTION_KEY = base64.urlsafe_b64encode(new_key).decode()
    # Save the key to the environment variable
    os.environ["ENCRYPTION_KEY"] = ENCRYPTION_KEY
    # Update the .env file with the new key
    set_key_in_env(ENCRYPTION_KEY)
else:
    print(f"Retrieved existing ENCRYPTION_KEY")

# Initialize the Fernet cipher suite with the encryption key
try:
    decoded_key = base64.urlsafe_b64decode(ENCRYPTION_KEY)
    cipher_suite = Fernet(decoded_key)
    print("Successfully initialized Fernet with the decoded key.")
except Exception as e:
    print(f"Failed to initialize Fernet with the key: {ENCRYPTION_KEY}, error: {e}")
    raise

# Encrypt a value
def encrypt_value(value):
    try:
        encrypted_value = cipher_suite.encrypt(value.encode('utf-8'))
        encoded_encrypted_value = base64.urlsafe_b64encode(encrypted_value).decode('utf-8')
        return encoded_encrypted_value
    except Exception as e:
        print(f"Error encrypting value, error: {e}")
        raise

# Decrypt a value
def decrypt_value(encrypted_value):
    try:
        decoded_encrypted_value = base64.urlsafe_b64decode(encrypted_value)
        decrypted_value = cipher_suite.decrypt(decoded_encrypted_value).decode('utf-8')
        return decrypted_value
    except Exception as e:
        print(f"Error decrypting value, error: {e}")
        return None

# Single API Keys
@jwt_required()
def get_single_api_key(api_key_name):
    current_user_id = get_jwt_identity()

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    
    if user_env and getattr(user_env, api_key_name, None):
        encrypted_value = getattr(user_env, api_key_name)
        display_value = decrypt_value(encrypted_value)
        return jsonify({"success": True, api_key_name: display_value}), 200
    else:
        return jsonify({"error": f"{api_key_name.capitalize()} API Key not found"}), 404

@jwt_required()
def save_single_api_key(api_key_name):
    current_user_id = get_jwt_identity()
    json_data = request.get_json()
    if not json_data or api_key_name not in json_data:
        return jsonify({"error": f"Missing {api_key_name.capitalize()} API Key"}), 400

    encrypted_value = encrypt_value(json_data[api_key_name])

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    if not user_env:
        user_env = UserEnv(user_id=current_user_id)

    setattr(user_env, api_key_name, encrypted_value)  # Set the attribute dynamically

    db.session.add(user_env)
    db.session.commit()

    return jsonify({"success": True, "message": f"{api_key_name.capitalize()} API Key saved successfully"}), 200

@jwt_required()
def update_single_api_key(api_key_name):
    current_user_id = get_jwt_identity()
    json_data = request.get_json()
    if not json_data or api_key_name not in json_data:
        return jsonify({"error": f"Missing {api_key_name.capitalize()} API Key"}), 400

    encrypted_value = encrypt_value(json_data[api_key_name])

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    if user_env:
        stored_value = decrypt_value(getattr(user_env, api_key_name))  # Decrypt stored value dynamically
        if not stored_value:
            return jsonify({"error": f"Error decrypting stored {api_key_name.capitalize()} API key"}), 500

        if stored_value != json_data[api_key_name]:
            setattr(user_env, api_key_name, encrypted_value)  # Update with new encrypted value dynamically
            db.session.commit()
            return jsonify({"success": True, "message": f"{api_key_name.capitalize()} API Key updated successfully"}), 200
        else:
            return jsonify({"success": True, "message": f"{api_key_name.capitalize()} API Key was the same"}), 200
    else:
        return jsonify({"error": f"{api_key_name.capitalize()} API Key not found"}), 404

@jwt_required()
def delete_single_api_key(api_key_name):
    current_user_id = get_jwt_identity()

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    if user_env and getattr(user_env, api_key_name):
        setattr(user_env, api_key_name, None)  # Set the attribute to None dynamically
        db.session.commit()
        return jsonify({"success": True, "message": f"{api_key_name.capitalize()} API Key deleted successfully"}), 200
    else:
        return jsonify({"error": f"{api_key_name.capitalize()} API Key not found"}), 404

# Dual API Keys
@jwt_required()
def get_dual_api_keys(api_key_name1, api_key_name2):
    current_user_id = get_jwt_identity()

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    if user_env and getattr(user_env, api_key_name1) and getattr(user_env, api_key_name2):
        key1_display = decrypt_value(getattr(user_env, api_key_name1))
        key2_display = decrypt_value(getattr(user_env, api_key_name2))
        return jsonify({
            "success": True,
            f"{api_key_name1}": key1_display,
            f"{api_key_name2}": key2_display
        }), 200
    else:
        return jsonify({"error": f"{api_key_name1.capitalize()} and {api_key_name2.capitalize()} not found"}), 404

@jwt_required()
def save_dual_api_keys(api_key_name1, api_key_name2):
    current_user_id = get_jwt_identity()
    json_data = request.get_json()
    if not json_data or not (api_key_name1 in json_data and api_key_name2 in json_data):
        return jsonify({"error": f"Missing {api_key_name1.capitalize()} or {api_key_name2.capitalize()}"}), 400

    encrypted_api_key1 = encrypt_value(json_data[api_key_name1])
    encrypted_api_key2 = encrypt_value(json_data[api_key_name2])

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    if not user_env:
        user_env = UserEnv(user_id=current_user_id)

    setattr(user_env, api_key_name1, encrypted_api_key1)
    setattr(user_env, api_key_name2, encrypted_api_key2)

    db.session.add(user_env)
    db.session.commit()

    return jsonify({"success": True, "message": f"{api_key_name1.capitalize()} and {api_key_name2.capitalize()} saved successfully"}), 200

@jwt_required()
def update_dual_api_keys(api_key_name1, api_key_name2):
    current_user_id = get_jwt_identity()
    json_data = request.get_json()
    if not json_data or not (api_key_name1 in json_data and api_key_name2 in json_data):
        return jsonify({"error": f"Missing {api_key_name1.capitalize()} or {api_key_name2.capitalize()}"}), 400

    encrypted_api_key1 = encrypt_value(json_data[api_key_name1])
    encrypted_api_key2 = encrypt_value(json_data[api_key_name2])

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    if user_env:
        stored_value1 = decrypt_value(getattr(user_env, api_key_name1))  # Decrypt stored value dynamically
        if not stored_value1:
            return jsonify({"error": f"Error decrypting stored {api_key_name1.capitalize()} API key"}), 500
        
        stored_value2 = decrypt_value(getattr(user_env, api_key_name2))  # Decrypt stored value dynamically
        if not stored_value2:
            return jsonify({"error": f"Error decrypting stored {api_key_name2.capitalize()} API key"}), 500
        
        # Check if current values match the new values
        if stored_value1 != json_data[api_key_name1] or stored_value2 != json_data[api_key_name2]:
            setattr(user_env, api_key_name1, encrypted_api_key1)  # Update with new encrypted value dynamically
            setattr(user_env, api_key_name2, encrypted_api_key2)
            db.session.commit()
            return jsonify({"success": True, "message": f"{api_key_name1.capitalize()} and {api_key_name2.capitalize()} updated successfully"}), 200
        else:
            return jsonify({"success": True, "message": f"{api_key_name1.capitalize()} and {api_key_name2.capitalize()} were the same"}), 200
    else:
        return jsonify({"error": f"{api_key_name1.capitalize()} and {api_key_name2.capitalize()} not found"}), 404

@jwt_required()
def delete_dual_api_keys(api_key_name1, api_key_name2):
    current_user_id = get_jwt_identity()

    user_env = UserEnv.query.filter_by(user_id=current_user_id).first()
    if user_env and (getattr(user_env, api_key_name1) or getattr(user_env, api_key_name2)):
        setattr(user_env, api_key_name1, None)
        setattr(user_env, api_key_name2, None)
        db.session.commit()
        return jsonify({"success": True, "message": f"{api_key_name1.capitalize()} and {api_key_name2.capitalize()} deleted successfully"}), 200
    else:
        return jsonify({"error": f"{api_key_name1.capitalize()} and {api_key_name2.capitalize()} not found"}), 404

# Single API Keys:
# Open AI
@jwt_required()
def save_open_ai_api_key():
    response = save_single_api_key("open_ai_api_key")
    return response
@jwt_required()   
def update_open_ai_api_key():
    response = update_single_api_key("open_ai_api_key")
    return response
@jwt_required()
def delete_open_ai_api_key():
    response = delete_single_api_key("open_ai_api_key")
    return response
@jwt_required()
def get_open_ai_api_key():
    response = get_single_api_key("open_ai_api_key")
    return response

# DomDetailer
@jwt_required()
def save_domdetailer_api_key():
    response = save_single_api_key("domdetailer_api_key")
    return response
@jwt_required()
def update_domdetailer_api_key():
    response = update_single_api_key("domdetailer_api_key")
    return response
@jwt_required()
def delete_domdetailer_api_key():
    response = delete_single_api_key("domdetailer_api_key")
    return response
@jwt_required()
def get_domdetailer_api_key():
    response = get_single_api_key("domdetailer_api_key")
    return response

# Dual API Keys
# Google
@jwt_required()
def save_google_api_keys():
    response = save_dual_api_keys("google_search_api_key", "google_cx")
    return response
@jwt_required()
def update_google_api_keys():
    response = update_dual_api_keys("google_search_api_key", "google_cx")
    return response
@jwt_required()
def delete_google_api_keys():
    response = delete_dual_api_keys("google_search_api_key", "google_cx")
    return response
@jwt_required()
def get_google_api_keys():
    response = get_dual_api_keys("google_search_api_key", "google_cx")
    return response

# Porkbun
@jwt_required()
def save_porkbun_api_keys():
    response = save_dual_api_keys("porkbun_api_key", "porkbun_secret")
    return response
@jwt_required()
def update_porkbun_api_keys():
    response = update_dual_api_keys("porkbun_api_key", "porkbun_secret")
    return response
@jwt_required()
def delete_porkbun_api_keys():
    response = delete_dual_api_keys("porkbun_api_key", "porkbun_secret")
    return response
@jwt_required()
def get_porkbun_api_keys():
    response = get_dual_api_keys("porkbun_api_key", "porkbun_secret")
    return response

# CZDS ICANN
@jwt_required()
def save_czds_credentials():
    response = save_dual_api_keys("czds_login", "czds_password")
    return response
@jwt_required()
def update_czds_credentials():
    response = update_dual_api_keys("czds_login", "czds_password")
    return response
@jwt_required()
def delete_czds_credentials():
    response = delete_dual_api_keys("czds_login", "czds_password")
    return response
@jwt_required()
def get_czds_credentials():
    response = get_dual_api_keys("czds_login", "czds_password")
    return response