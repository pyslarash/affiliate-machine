from database.models import UserEnv
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
import re
import os
from dotenv import load_dotenv
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Ollama settings

def validate_ollama_credentials(ollama_ip, ollama_port):
    ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if not ip_pattern.match(ollama_ip):
        return False, "Invalid IP address format. It should be in the form x.x.x.x"
    
    if not (str(ollama_port).isdigit() and 0 < int(ollama_port) <= 99999):
        return False, "Invalid port. It should be a digit up to 5 digits long."
    
    return True, ""

def validate_ollama_web_address(web_address):
    if web_address.startswith(('http://', 'https://')):
        return True, 'Valid web address'
    return False, 'Invalid web address. It must start with http:// or https://'

# IP and Port

@jwt_required()
def set_ollama_credentials():
    user_id = get_jwt_identity()
    ollama_ip = request.json.get('ollama_ip')
    ollama_port = request.json.get('ollama_port')
    is_valid, message = validate_ollama_credentials(ollama_ip, ollama_port)
    if not is_valid:
        return {'message': message}, 400

    # Check if credentials already exist
    existing_credentials = UserEnv.query.filter_by(user_id=user_id).first()
    if existing_credentials:
        return {'message': 'Credentials already exist for this user. Refresh the page.'}, 400

    # Add new credentials
    user_env = UserEnv(user_id=user_id, ollama_ip=ollama_ip, ollama_port=ollama_port)
    db.session.add(user_env)
    db.session.commit()
    return {'message': 'Credentials set successfully'}, 201

@jwt_required()
def update_ollama_credentials():
    user_id = get_jwt_identity()
    ollama_ip = request.json.get('ollama_ip')
    ollama_port = request.json.get('ollama_port')

    is_valid, message = validate_ollama_credentials(ollama_ip, ollama_port)
    if not is_valid:
        return {'message': message}, 400

    # Update existing credentials if they exist
    user_env = UserEnv.query.filter_by(user_id=user_id).first()
    if user_env:
        user_env.ollama_ip = ollama_ip
        user_env.ollama_port = ollama_port
        db.session.commit()
        return {'message': 'Credentials updated successfully'}, 200
    else:
        return {'message': 'No credentials found for this user'}, 404

@jwt_required()
def delete_ollama_credentials():
    user_id = get_jwt_identity()
    user_env = UserEnv.query.filter_by(user_id=user_id).first()
    try:
        if user_env:
            user_env.ollama_ip = None
            user_env.ollama_port = None
            db.session.commit()
            return {'message': 'Credentials deleted successfully'}, 200
        return {'message': 'No credentials found for this user'}, 404
    finally:
        db.session.close()

@jwt_required()  # Protect this route with JWT authentication
def get_ollama_credentials():
    try:
        user_id = get_jwt_identity()
        user_env = UserEnv.query.filter_by(user_id=user_id).first()

        if user_env:
            return jsonify({
                'ollama_ip': user_env.ollama_ip,
                'ollama_port': user_env.ollama_port
            }), 200
        else:
            return jsonify({'message': 'No Ollama credentials found for this user'}), 404
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
# Web address

@jwt_required()
def set_ollama_web():
    user_id = get_jwt_identity()
    ollama_web_address = request.json.get('ollama_web_address')

    is_valid, message = validate_ollama_web_address(ollama_web_address)
    if not is_valid:
        return {'message': message}, 400

    # Check if credentials already exist
    existing_credentials = UserEnv.query.filter_by(user_id=user_id).first()
    if existing_credentials:
        return {'message': 'Web address already exist for this user. Refresh the page.'}, 400

    # Add new credentials
    user_env = UserEnv(user_id=user_id, ollama_web_address=ollama_web_address)
    db.session.add(user_env)
    db.session.commit()
    return {'message': 'Web address set successfully'}, 201

@jwt_required()
def update_ollama_web():
    user_id = get_jwt_identity()
    ollama_web_address = request.json.get('ollama_web_address')

    is_valid, message = validate_ollama_web_address(ollama_web_address)
    if not is_valid:
        return {'message': message}, 400

    # Update existing credentials if they exist
    user_env = UserEnv.query.filter_by(user_id=user_id).first()
    if user_env:
        user_env.ollama_web_address = ollama_web_address
        db.session.commit()
        return {'message': 'Web address updated successfully'}, 200
    else:
        return {'message': 'No web address found for this user'}, 404

@jwt_required()
def delete_ollama_web():
    user_id = get_jwt_identity()
    user_env = UserEnv.query.filter_by(user_id=user_id).first()
    try:
        if user_env:
            user_env.ollama_web_address = None
            db.session.commit()
            return {'message': 'Web address deleted successfully'}, 200
        return {'message': 'No web address found for this user'}, 404
    finally:
        db.session.close()

@jwt_required()  # Protect this route with JWT authentication
def get_ollama_web():
    try:
        user_id = get_jwt_identity()
        user_env = UserEnv.query.filter_by(user_id=user_id).first()

        if user_env:
            return jsonify({
                'ollama_web_address': user_env.ollama_web_address
            }), 200
        else:
            return jsonify({'message': 'No Ollama web address found for this user'}), 404
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    

#############
# Make sure to combine the functionality of adding IP+Port or Web. Like if user adds all 3, don't let them do it! Don't write anything into DB unless they fix it. Throw messages to the front end. Simplify it to just 4 global API calls.