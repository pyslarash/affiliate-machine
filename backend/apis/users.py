import os
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from argon2 import PasswordHasher, exceptions
from database.models import User, TokenBlacklist
from database.token_cleanup import automatic_remove_token
from database import db
from .components.user_checks import is_valid_email, is_valid_password, is_admin, get_current_user, authorized_to_create_admin, check_user_permissions
from werkzeug.exceptions import Forbidden, NotFound
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import uuid

load_dotenv()

app = Flask(__name__)

ph = PasswordHasher()
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Internal flag to prevent setting user_type to 'admin' outside create_admin function
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    requested_user_type = data.get('user_type', 'user')  # Default to 'user'

    # Validate input fields
    if not all([email, password, username]):
        return jsonify({'message': 'Missing required fields'}), 400

    if not is_valid_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    if not is_valid_password(password):
        return jsonify({'message': 'Password requirements not met'}), 400

    # Check if someone is trying to set user_type to 'admin'
    if requested_user_type == "admin":
        return jsonify({'message': 'Not so fast, Speedy Gonzales!'}), 403

    hashed_password = ph.hash(password)

    new_user = User(email=email, password=hashed_password, username=username, user_type=requested_user_type)
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Email or username already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    
# Now your create_admin function would look like this
def create_admin():
    if not authorized_to_create_admin():
        return jsonify({'message': 'Unauthorized or invalid passcode'}), 403
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    # Internally set user_type to 'admin'
    user_type = 'admin'
    hashed_password = ph.hash(password)

    new_user = User(email=email, password=hashed_password, username=username, first_name=first_name, last_name=last_name, user_type=user_type)
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify({'message': 'Admin user created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Email or username already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    
# Login User
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({'message': 'Invalid username or password'}), 401

    try:
        ph.verify(user.password, password)
    except exceptions.VerifyMismatchError:
        return jsonify({'message': 'Invalid username or password'}), 401

    # Check for existing active tokens
    now = datetime.now(timezone.utc)
    active_token = TokenBlacklist.query.filter(
        TokenBlacklist.user_id == user.id,
        TokenBlacklist.expires_at > now,
        TokenBlacklist.is_active == True
    ).first()
    if active_token:
        return jsonify({'message': 'User already logged in'}), 400

    # If password verification is successful, generate a JWT
    exp_time = now + timedelta(hours=24)  # Token expires in 24 hours
    token_payload = {
        'sub': user.id,
        'exp': exp_time,
        'jti': str(uuid.uuid4())  # Unique identifier for the token
    }
    token = jwt.encode(token_payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")

    new_active_token = TokenBlacklist(token=token, jti=token_payload['jti'], user_id=user.id, expires_at=exp_time, is_active=True)
    db.session.add(new_active_token)
    expiration_time = exp_time.isoformat()
    user_id = user.id
    try:
        db.session.commit()
        # Include expiration time in the response
        return jsonify({'token': token, 'expiration_time': expiration_time, 'user_id': user_id}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to log in'}), 500

@jwt_required()
def logout_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id and not User.query.get(current_user_id).user_type == 'admin':
        raise Forbidden(description='Unauthorized - Cannot log out other users')

    token_jti = get_jwt()['jti']
    print(f"Token JTI from JWT: {token_jti}")  # Check the JTI extracted from the token

    if token_jti is None:
        return jsonify({'message': 'Invalid token'}), 400

    # Find the token and check its active status
    token_to_deactivate = TokenBlacklist.query.filter_by(jti=token_jti, is_active=True).first()
    if not token_to_deactivate:
        print(f"No active token found for JTI: {token_jti}")  # Log if no token found or if not active
        return jsonify({'message': 'Token not active or already logged out'}), 400

    print("Token found and will be deactivated.")  # Confirmation before deactivation
    token_to_deactivate.is_active = False
    try:
        db.session.commit()
        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    
# Delete a user
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    jwt_identifier = get_jwt()['jti']  # Get the unique identifier of the JWT

    # Check if the token has been blacklisted
    token_in_blacklist = TokenBlacklist.query.filter_by(jti=jwt_identifier, is_active=False).first()
    if token_in_blacklist:
        return jsonify({'message': 'Cannot delete user as the user is logged out'}), 403

    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'Current user not found'}), 404

    print(f"Current user ID: {current_user_id}, Role: {current_user.user_type}, Target User ID: {user_id}")

    if not (current_user.user_type == 'admin' or current_user_id == int(user_id)):
        return jsonify({'message': 'No permission to delte this user.'}), 403

    user_to_delete = User.query.get(user_id)
    if not user_to_delete:
        raise NotFound(description='User not found')

    db.session.delete(user_to_delete)
    try:
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# Modify a user
@jwt_required()
def edit_user(user_id):
    current_user_id = get_jwt_identity()
    jwt_identifier = get_jwt()['jti']  # Get the unique identifier of the JWT
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'Current user not found'}), 404

    if not (current_user.user_type == 'admin' or current_user_id == int(user_id)):
        return jsonify({'message': 'Unauthorized'}), 403
    
    # Check if the token has been blacklisted
    token_in_blacklist = TokenBlacklist.query.filter_by(jti=jwt_identifier, is_active=False).first()
    if token_in_blacklist:
        return jsonify({'message': 'Cannot edit profile as the user is logged out'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User to edit not found'}), 404

    data = request.json
    
    # Update user fields if provided
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    user_type = data.get('user_type')
    
    if email and is_valid_email(email):
        user.email = email
    if password and is_valid_password(password):
        user.password = ph.hash(password)
    else:
        return jsonify({'message': 'Invalid password format'}), 400
    if username:
        user.username = username
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if user_type and current_user.user_type == 'admin':
        user.user_type = user_type
    elif user_type:
        return jsonify({'message': 'Unauthorized to change user type'}), 403

    try:
        db.session.commit()
        return jsonify({'message': 'User modified successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Email or username already exists', 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# Get information about a single user
@jwt_required()
def get_user_info(user_id):
    jwt_identifier = get_jwt()['jti']  # Get the unique identifier of the JWT

    # Check if the token has been blacklisted
    token_in_blacklist = TokenBlacklist.query.filter_by(jti=jwt_identifier, is_active=False).first()
    if token_in_blacklist:
        return jsonify({'message': 'Access denied - User is logged out'}), 403

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'Current user not found'}), 404

    if current_user.user_type != 'admin' and current_user_id != int(user_id):
        return jsonify({'message': 'Unauthorized - Access is restricted to your own information'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_info = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type': user.user_type
    }

    return jsonify(user_info), 200

# Get all users (for admin)
@jwt_required()
def get_all_users():
    jwt_identifier = get_jwt()['jti']  # Get the unique identifier of the JWT

    # Check if the token has been blacklisted
    token_in_blacklist = TokenBlacklist.query.filter_by(jti=jwt_identifier, is_active=False).first()
    if token_in_blacklist:
        return jsonify({'message': 'Access denied - User is logged out'}), 403

    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({'message': 'Current user not found'}), 404

    if current_user.user_type != 'admin':
        return jsonify({'message': 'Unauthorized - Only admins can access all user data'}), 403

    users = User.query.all()
    users_info = [{
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_type': user.user_type
    } for user in users]

    return jsonify(users_info), 200