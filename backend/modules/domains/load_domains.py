from flask import jsonify, request
from modules.czds.czds import display_zonefile_contents
from database.models import Domains, db

# This function imports domains from the Zone file and checks if the domain has been imported already
def import_domains(zone):
    response, status_code = display_zonefile_contents(zone)
    
    if status_code == 200:
        domains_list = response.json['domains']
        added_count = 0
        skipped_count = 0
        
        for domain in domains_list:
            existing_domain = Domains.query.filter_by(domain=domain).first()
            if not existing_domain:
                new_domain = Domains(domain=domain, zone=zone.lower())
                db.session.add(new_domain)
                added_count += 1
            else:
                skipped_count += 1

        db.session.commit()
        
        return jsonify({
            'message': 'Domains processed successfully.',
            'added': added_count,
            'skipped': skipped_count
        }), 200
    else:
        return jsonify({'error': 'Failed to load domains.'}), status_code
    
# Imports domains provided by a user in a JSON format
def set_domains_from_json():
    try:
        data = request.get_json()
        domains_list = data.get('domains', [])

        if not domains_list:
            return jsonify({'error': 'No domains provided in JSON payload.'}), 400

        added_count = 0
        skipped_count = 0

        for domain in domains_list:
            existing_domain = Domains.query.filter_by(domain=domain).first()
            if not existing_domain:
                # Determine zone from domain
                if '.' in domain:
                    zone = domain.rsplit('.', 1)[-1].lower()  # Get last part after dot in lowercase
                else:
                    zone = None  # Handle cases where domain may not have a zone

                new_domain = Domains(domain=domain.lower(), zone=zone)
                db.session.add(new_domain)
                added_count += 1
            else:
                skipped_count += 1

        db.session.commit()

        return jsonify({
            'message': 'Domains processed successfully.',
            'added': added_count,
            'skipped': skipped_count
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to process domains: {str(e)}'}), 500

# Removes a single domain from the database
def remove_domain(domain_name):
    domain = Domains.query.filter_by(domain=domain_name).first()
    if domain:
        db.session.delete(domain)
        db.session.commit()
        return jsonify({'message': f'Domain {domain_name} deleted successfully.'}), 200
    else:
        return jsonify({'error': f'Domain {domain_name} not found.'}), 404

# Removes entire zone from the database   
def remove_zone(zone):
    domains = Domains.query.filter_by(zone=zone).all()
    if domains:
        count = len(domains)
        for domain in domains:
            db.session.delete(domain)
        db.session.commit()
        return jsonify({'message': f'{count} domains under zone {zone} deleted successfully.'}), 200
    else:
        return jsonify({'error': f'No domains found under zone {zone}.'}), 404