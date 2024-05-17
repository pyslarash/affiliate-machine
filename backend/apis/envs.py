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

# Save or update one or more ENV values
@jwt_required()
def save_or_update_env_values():
    current_user_id = get_jwt_identity()

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Missing JSON data"}), 400

    if isinstance(json_data, dict):
        json_data = [json_data]

    if not isinstance(json_data, list):
        return jsonify({"error": "Input data must be a list of ENVs"}), 400

    for env_data in json_data:
        if "name" not in env_data or "value" not in env_data:
            return jsonify({"error": "Name and value are required fields in each ENV"}), 400

        name = env_data["name"]
        value = env_data["value"]
        codename = name.lower().replace(" ", "-")
        encrypted_value = encrypt_value(value)

        existing_entry = UserEnv.query.filter_by(user_id=current_user_id, codename=codename).first()

        if existing_entry:
            existing_entry.value = encrypted_value
        else:
            new_entry = UserEnv(user_id=current_user_id, name=name, codename=codename, value=encrypted_value)
            db.session.add(new_entry)

    db.session.commit()

    return jsonify({"success": True, "message": "All ENVs saved or updated successfully"}), 200

# Get the value for an API key in JSON format
@jwt_required()
def get_api_key_value(codename):
    current_user_id = get_jwt_identity()
    api_key_entry = UserEnv.query.filter_by(user_id=current_user_id, codename=codename).first()

    if api_key_entry:
        try:
            decrypted_value = decrypt_value(api_key_entry.value)
            if decrypted_value:
                return jsonify({"success": True, "value": decrypted_value}), 200
            else:
                return jsonify({"error": "Error decrypting the value"}), 500
        except Exception as e:
            print(f"Error during decryption: {e}")
            return jsonify({"error": "Error decrypting the value"}), 500
    else:
        return jsonify({"error": f"API key '{codename}' not found"}), 404

# Get all ENVs associated with a specific user
@jwt_required()
def get_user_envs():
    current_user_id = get_jwt_identity()
    user_envs = UserEnv.query.filter_by(user_id=current_user_id).all()

    envs_data = []
    for env in user_envs:
        try:
            decrypted_value = decrypt_value(env.value)
            if decrypted_value:
                masked_value = '*' * (len(decrypted_value) - 4) + decrypted_value[-4:]
            else:
                masked_value = "Error decrypting the value"
            envs_data.append({"name": env.name, "codename": env.codename, "value": masked_value})
        except Exception as e:
            print(f"Error decrypting value for {env.codename}: {e}")
            envs_data.append({"name": env.name, "codename": env.codename, "value": "Error decrypting the value"})

    return jsonify({"success": True, "envs": envs_data}), 200

# Delete an API key based on codename
@jwt_required()
def delete_env(codename):
    current_user_id = get_jwt_identity()
    api_key_entry = UserEnv.query.filter_by(user_id=current_user_id, codename=codename).first()

    if api_key_entry:
        db.session.delete(api_key_entry)
        db.session.commit()
        return jsonify({"success": True, "message": "API key deleted successfully"}), 200
    else:
        return jsonify({"error": f"API key '{codename}' not found for the current user"}), 404
