from flask import Flask
from apis.users import create_user, create_admin, edit_user, delete_user, login_user, logout_user, get_user_info, get_all_users
from apis.envs import save_or_update_env_values, get_api_key_value, get_user_envs, delete_env

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
    # Saving or getting the ENVs for a specific user
    app.route('/save_update_envs', methods=['POST'])(save_or_update_env_values)
    app.route('/get_single_env/<string:codename>', methods=['GET'])(get_api_key_value)
    app.route('/get_envs', methods=['GET'])(get_user_envs)
    app.route('/delete_single_env/<string:codename>', methods=['DELETE'])(delete_env)