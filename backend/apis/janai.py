from database.models import UserEnv
from database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Flask, request, jsonify
import re
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Jan.ai settings

def validate_jan_credentials(jan_ip, jan_port, jan_prefix):
    ip_pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if not ip_pattern.match(jan_ip):
        return False, "Invalid IP address format. It should be in the form x.x.x.x"
    
    if not (str(jan_port).isdigit() and 0 < int(jan_port) <= 99999):
        return False, "Invalid port. It should be a digit up to 5 digits long."
    
    if not jan_prefix.startswith("/"):
        return False, "Invalid prefix. It should start with '/'."
    
    return True, ""

@jwt_required()
def set_credentials():
    user_id = get_jwt_identity()
    jan_ip = request.json.get('jan_ip')
    jan_port = request.json.get('jan_port')
    jan_prefix = request.json.get('jan_prefix')

    is_valid, message = validate_jan_credentials(jan_ip, jan_port, jan_prefix)
    if not is_valid:
        return {'message': message}, 400

    # Check if credentials already exist
    existing_credentials = UserEnv.query.filter_by(user_id=user_id).first()
    if existing_credentials:
        return {'message': 'Credentials already exist for this user. Refresh the page.'}, 400

    # Add new credentials
    user_env = UserEnv(user_id=user_id, jan_ip=jan_ip, jan_port=jan_port, jan_prefix=jan_prefix)
    db.session.add(user_env)
    db.session.commit()
    return {'message': 'Credentials set successfully'}, 201

@jwt_required()
def update_credentials():
    user_id = get_jwt_identity()
    jan_ip = request.json.get('jan_ip')
    jan_port = request.json.get('jan_port')
    jan_prefix = request.json.get('jan_prefix')

    is_valid, message = validate_jan_credentials(jan_ip, jan_port, jan_prefix)
    if not is_valid:
        return {'message': message}, 400

    # Update existing credentials if they exist
    user_env = UserEnv.query.filter_by(user_id=user_id).first()
    if user_env:
        user_env.jan_ip = jan_ip
        user_env.jan_port = jan_port
        user_env.jan_prefix = jan_prefix
        db.session.commit()
        return {'message': 'Credentials updated successfully'}, 200
    else:
        return {'message': 'No credentials found for this user'}, 404

@jwt_required()
def delete_credentials():
    user_id = get_jwt_identity()
    user_env = UserEnv.query.filter_by(user_id=user_id).first()
    if user_env:
        db.session.delete(user_env)
        db.session.commit()
        return {'message': 'Credentials deleted successfully'}, 200
    return {'message': 'No credentials found for this user'}, 404

@jwt_required()  # Protect this route with JWT authentication
def get_credentials():
    try:
        user_id = get_jwt_identity()
        user_env = UserEnv.query.filter_by(user_id=user_id).first()

        if user_env:
            return jsonify({
                'jan_ip': user_env.jan_ip,
                'jan_port': user_env.jan_port,
                'jan_prefix': user_env.jan_prefix
            }), 200
        else:
            return jsonify({'message': 'No Jan.ai credentials found for this user'}), 404
    
    except Exception as e:
        return jsonify({'message': str(e)}), 500