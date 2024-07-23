from flask import Flask
from apis.users import *
from apis.janai import *
from apis.api_keys import *
from modules.czds.czds import *
from modules.domains.load_domains import *
from modules.domains.set_domains import *
from modules.domains.domain_check import *
from modules.domains.domdetailer import *

# Routes for the user-related functionality

def api(app):
    # USER ROUTES
    app.route('/create_user', methods=['POST'])(create_user)
    app.route('/create_admin', methods=['POST'])(create_admin)
    app.route('/login_user', methods=['POST'])(login_user)
    app.route('/logout_user/<int:user_id>', methods=['POST'])(logout_user)
    app.route('/edit_user/<int:user_id>', methods=['PUT'])(edit_user)
    app.route('/delete_user/<int:user_id>', methods=['DELETE'])(delete_user)
    app.route('/get_user/<int:user_id>', methods=['GET'])(get_user_info)
    app.route('/get_all_users', methods=['GET'])(get_all_users)
    
    #######################################################################

    # ROUTES FOR JAN.AI
    app.route('/set_credentials', methods=['POST'])(set_credentials)
    app.route('/update_credentials', methods=['PUT'])(update_credentials)
    app.route('/delete_credentials', methods=['DELETE'])(delete_credentials)
    app.route('/get_credentials', methods=['GET'])(get_credentials)
    
    #######################################################################

    # ROUTES FOR API KEYS
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
    app.route('/get_domdetailer_api_key', methods=['GET'])(get_domdetailer_api_key)
    app.route('/save_domdetailer_api_key', methods=['POST'])(save_domdetailer_api_key)
    app.route('/update_domdetailer_api_key', methods=['PUT'])(update_domdetailer_api_key)
    app.route('/delete_domdetailer_api_key', methods=['DELETE'])(delete_domdetailer_api_key)
    
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
    
    #######################################################################
    
    # DOMAIN ROUTES    
    # CZDS zonefiles
    app.route('/get_czds_zonefiles_list', methods=['GET'])(get_czds_zonefiles_list)
    app.route('/get_czds_zonefiles_heads/<zone>', methods=['GET'])(get_czds_zonefiles_heads)
    app.route('/download_czds_zonefile/<zone>', methods=['GET'])(download_czds_zonefile)
    app.route('/display_zonefile_contents/<zone>', methods=['GET'])(display_zonefile_contents)
    
    # Domains
    app.route('/import_domains/<zone>', methods=['POST'])(import_domains)
    app.route('/set_domains_from_json', methods=['POST'])(set_domains_from_json)
    app.route('/remove_domain/<domain_name>', methods=['DELETE'])(remove_domain)
    app.route('/remove_zone/<zone>', methods=['DELETE'])(remove_zone)
    
    # Setting domains
    app.route('/domain_whois_check/<domain_name>', methods=['GET'])(domain_whois_check)
    app.route('/set_domains', methods=['POST'])(set_domains)
    app.route('/check_unavailable_domains', methods=['POST'])(check_unavailable_domains)
    app.route('/check_available_domains', methods=['POST'])(check_available_domains)
    app.route('/get_available_domains', methods=['GET'])(get_available_domains)
    app.route('/get_unavailable_domains', methods=['GET'])(get_unavailable_domains)
    
    # app.route('/domain_info_check/<domain_name>', methods=['GET'])(domain_info_check)
    
    # DomDetailer
    app.route('/check_domdetailer_balance', methods=['GET'])(check_domdetailer_balance)
    app.route('/check_domdetailer_domain/<domain_name>', methods=['GET'])(check_domdetailer_domain)