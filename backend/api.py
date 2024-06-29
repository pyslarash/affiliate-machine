from flask import Flask
from apis.users import create_user, create_admin, edit_user, delete_user, login_user, logout_user, get_user_info, get_all_users
from apis.envs import set_credentials, update_credentials, delete_credentials, get_credentials

def user_routes(app):
    # Register the create_user function with the /create_user endpoint
    app.route('/create_user', methods=['POST'])(create_user)
    app.route('/create_admin', methods=['POST'])(create_admin)
    app.route('/login_user', methods=['POST'])(login_user)
    app.route('/logout_user/<int:user_id>', methods=['POST'])(logout_user)
    app.route('/edit_user/<int:user_id>', methods=['PUT'])(edit_user)
    app.route('/delete_user/<int:user_id>', methods=['DELETE'])(delete_user)
    app.route('/get_user/<int:user_id>', methods=['GET'])(get_user_info)
    app.route('/get_all_users', methods=['GET'])(get_all_users)

def env_values(app):
    app.route('/set_credentials', methods=['POST'])(set_credentials)
    app.route('/update_credentials', methods=['PUT'])(update_credentials)
    app.route('/delete_credentials', methods=['DELETE'])(delete_credentials)
    app.route('/get_credentials', methods=['GET'])(get_credentials)
