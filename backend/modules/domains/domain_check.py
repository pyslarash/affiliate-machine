import whoisdomain as whois
from flask import jsonify
import seolib

def domain_whois_check(domain_name):
    try:
        domain_info = whois.query(domain_name)
        
        if domain_info == None:
            return jsonify({'status': 'available', 'domain': domain_name}), 200
        
        expiration_datetime = domain_info.expiration_date
        if isinstance(expiration_datetime, list):
            expiration_datetime = expiration_datetime[0]
            
        creation_datetime = domain_info.creation_date
        if isinstance(creation_datetime, list):
            creation_datetime = creation_datetime[0]
            
        updated_datetime = domain_info.last_updated
        if isinstance(updated_datetime, list):
            updated_datetime = updated_datetime[0]
            
        name_servers = domain_info.name_servers
        if not isinstance(name_servers, list):
            name_servers = [name_servers]
            
        name_servers = [ns.rstrip('.') for ns in name_servers]
            
        domain_record = {
            'domain': domain_name,
            'expiration_date': expiration_datetime.strftime('%Y-%m-%d') if expiration_datetime else None,
            'expiration_time': expiration_datetime.strftime('%H:%M:%S') if expiration_datetime else None,
            'creation_date': creation_datetime.strftime('%Y-%m-%d') if creation_datetime else None,
            'creation_time': creation_datetime.strftime('%H:%M:%S') if creation_datetime else None,
            'updated_date': updated_datetime.strftime('%Y-%m-%d') if updated_datetime else None,
            'updated_time': updated_datetime.strftime('%H:%M:%S') if updated_datetime else None,
            'name_servers': name_servers if name_servers else None
        }
        
        if domain_record['expiration_date']:
            return jsonify({'domain': domain_record, 'status': 'unavailable'}), 200
        else:
            return jsonify({'error': 'Expiration date not found for the domain.'}), 404
    except Exception as e:
        return jsonify({'error': f'Error fetching WHOIS data for domain {domain_name}: {str(e)}'}), 500
    
def domain_info_check(domain_name):
    semrush = seolib.get_semrush(domain_name)
        
    return jsonify({'semrush': semrush}), 200