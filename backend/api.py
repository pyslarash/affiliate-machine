from flask import Flask
from apis.users import *
from apis.janai import *
from apis.api_keys import *
from modules.czds.czds import *

from apis.components.api_key_decoder import api_key_decoder
# Routes for the user-related functionality
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

# Routes for Jan.ai
def jan_ai(app):
    app.route('/set_credentials', methods=['POST'])(set_credentials)
    app.route('/update_credentials', methods=['PUT'])(update_credentials)
    app.route('/delete_credentials', methods=['DELETE'])(delete_credentials)
    app.route('/get_credentials', methods=['GET'])(get_credentials)

# Routes for API keys
def api_keys(app):
    # OpenAI API key routes
    app.route('/get_open_ai_api_key', methods=['GET'])(get_open_ai_api_key)
    app.route('/save_open_ai_api_key', methods=['POST'])(save_open_ai_api_key)
    app.route('/update_open_ai_api_key', methods=['PUT'])(update_open_ai_api_key)
    app.route('/delete_open_ai_api_key', methods=['DELETE'])(delete_open_ai_api_key)    

    # Google API keys routes
    app.route('/get_google_api_keys', methods=['GET'])(get_google_api_keys)
    app.route('/save_google_api_keys', methods=['POST'])(save_google_api_keys)
    app.route('/update_google_api_keys', methods=['PUT'])(update_google_api_keys)
    app.route('/delete_google_api_keys', methods=['DELETE'])(delete_google_api_keys)
    

    # MyAddr API key routes
    app.route('/get_myaddr_api_key', methods=['GET'])(get_myaddr_api_key)
    app.route('/save_myaddr_api_key', methods=['POST'])(save_myaddr_api_key)
    app.route('/update_myaddr_api_key', methods=['PUT'])(update_myaddr_api_key)
    app.route('/delete_myaddr_api_key', methods=['DELETE'])(delete_myaddr_api_key)
    

    # Porkbun API keys routes
    app.route('/get_porkbun_api_keys', methods=['GET'])(get_porkbun_api_keys)
    app.route('/save_porkbun_api_keys', methods=['POST'])(save_porkbun_api_keys)
    app.route('/update_porkbun_api_keys', methods=['PUT'])(update_porkbun_api_keys)
    app.route('/delete_porkbun_api_keys', methods=['DELETE'])(delete_porkbun_api_keys)    
    
    # CZDS credentials routes
    app.route('/get_czds_credentials', methods=['GET'])(get_czds_credentials)
    app.route('/save_czds_credentials', methods=['POST'])(save_czds_credentials)
    app.route('/update_czds_credentials', methods=['PUT'])(update_czds_credentials)
    app.route('/delete_czds_credentials', methods=['DELETE'])(delete_czds_credentials)
    
def czds(app):
    app.route('/get_czds_zonefiles_list', methods=['GET'])(get_czds_zonefiles_list)
    app.route('/get_czds_zonefiles_heads/<zone>', methods=['GET'])(get_czds_zonefiles_heads)
    app.route('/download_czds_zonefile/<zone>', methods=['GET'])(download_czds_zonefile)
    app.route('/display_zonefile_contents/<zone>', methods=['GET'])(display_zonefile_contents)
    app.route('/zonefile_with_expiration/<zone>', methods=['GET'])(zonefile_with_expiration)