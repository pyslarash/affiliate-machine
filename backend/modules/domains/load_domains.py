from flask import jsonify
from modules.czds.czds import display_zonefile_contents
from database.models import Domains, db

def set_domains(zone):
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

def remove_domain(domain_name):
    domain = Domains.query.filter_by(domain=domain_name).first()
    if domain:
        db.session.delete(domain)
        db.session.commit()
        return jsonify({'message': f'Domain {domain_name} deleted successfully.'}), 200
    else:
        return jsonify({'error': f'Domain {domain_name} not found.'}), 404
    
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