from datetime import datetime, timezone
from flask import jsonify, current_app
import whois
from database.models import db, UnavailableDomains, Domains
from sqlalchemy.orm import sessionmaker

# Define the session
Session = sessionmaker()

# Single domain whois check
def domain_whois_check(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        
        expiration_datetime = domain_info.expiration_date
        if isinstance(expiration_datetime, list):
            expiration_datetime = expiration_datetime[0]
            
        creation_datetime = domain_info.creation_date
        if isinstance(creation_datetime, list):
            creation_datetime = creation_datetime[0]
            
        updated_datetime = domain_info.updated_date
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
            return jsonify({'domain': domain_record}), 200
        else:
            return jsonify({'error': 'Expiration date not found for the domain.'}), 404
    except Exception as e:
        return jsonify({'error': f'Error fetching WHOIS data for domain {domain_name}: {str(e)}'}), 500
 
# Updating unavailable domains table   
def update_unavailable_domains():
    # Ensure you're within the Flask application context
    with current_app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()

        domains = session.query(Domains).all()

        new_domains_count = 0
        skipped_domains_count = 0

        for domain in domains:
            domain_name = domain.domain

            existing_entry = session.query(UnavailableDomains).filter(UnavailableDomains.domain_id == domain.id).first()

            if existing_entry:
                skipped_domains_count += 1
                continue

            try:
                response, status_code = domain_whois_check(domain_name)
                
                if status_code == 200:
                    
                    domain_info = response.get_json().get('domain')

                    if domain_info['expiration_date']:
                        unavailable_domain = UnavailableDomains(
                            domain_id=domain.id,
                            creation_date=domain_info['creation_date'],
                            creation_time=domain_info['creation_time'],
                            expiration_date=domain_info['expiration_date'],
                            expiration_time=domain_info['expiration_time'],
                            name_servers=', '.join(domain_info['name_servers']) if domain_info['name_servers'] else None,
                            updated_date=domain_info['updated_date'],
                            updated_time=domain_info['updated_time'],
                            last_updated=datetime.now(timezone.utc)
                        )

                        session.add(unavailable_domain)
                        new_domains_count += 1
                        
                    else:
                        continue
            except Exception as e:
                print(f"Error fetching WHOIS data for domain {domain_name}: {str(e)}")

        session.commit()

    return jsonify({
        'message': 'Domains processed successfully.',
        'new_domains_added': new_domains_count,
        'domains_skipped': skipped_domains_count
    }), 200