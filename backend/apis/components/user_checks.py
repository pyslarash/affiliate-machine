import re
import regex
from flask import g
from database.models import User
import os
from dotenv import load_dotenv
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from flask import g 
from werkzeug.exceptions import Forbidden, NotFound

load_dotenv()

# Check if email is valid
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# Check if password is valid
def is_valid_password(password):
    # Pattern includes checking for any special character now
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^\w\s])[A-Za-z\d\s\p{P}\p{S}]{10,}$'
    if regex.search(pattern, password):
        return True
    else:
        return False

# Getting current user
def get_current_user():
    # Assuming 'user_id' is stored in Flask's global g object during authentication
    if not hasattr(g, 'user_id'):
        return None  # No user is logged in
    return User.query.get(g.user_id)

# Checking adminniness
def is_admin(user):
    # Check if the user's type or role is 'admin'
    return user.user_type == 'admin'

# Function to check if the user is authorized to create an admin
def authorized_to_create_admin():
    # Retrieve the passcode from the environment variables
    admin_passcode = os.getenv('ADMIN_CREATION_PASSCODE')
    # Get passcode from request headers or json body
    provided_passcode = request.headers.get('X-Admin-Passcode') or request.json.get('admin_passcode')

    # Compare the provided passcode with the one in the environment
    if provided_passcode == admin_passcode:
        return True
    return False


def check_user_permissions(user_id, require_admin=False):
    """
    Check if the current user is allowed to manipulate the specified user account.
    - user_id: the ID of the user to manipulate.
    - require_admin: set to True if the operation should only be performed by an admin.
    """
    current_user = User.query.get(get_jwt_identity())
    g.current_user = current_user  # Store current user in global context for further use in request lifecycle

    if current_user is None:
        raise NotFound(description="Current user not found.")

    if require_admin and not current_user.user_type == 'admin':
        raise Forbidden(description="Insufficient permissions - Admin required.")

    if not require_admin and current_user.user_type != 'admin' and current_user.id != user_id:
        raise Forbidden(description="Insufficient permissions - Not allowed to manipulate another user's account.")