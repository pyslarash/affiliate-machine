from datetime import datetime, timezone
from flask import jsonify, current_app
from database.models import db, UnavailableDomains, Domains, AvailableDomains
from modules.domains.domain_check import *
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import jwt_required

# Define the session
Session = sessionmaker()

# Adding new domains
def set_domains():
    with current_app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        domains = session.query(Domains).all()
        
        available_domains_count = 0
        unavailable_domains_count = 0
        skipped_available_domains_count = 0
        skipped_unavailable_domains_count = 0
        
        try:
            for domain in domains:
                domain_name = domain.domain
                
                existing_available_entry = session.query(AvailableDomains).filter(AvailableDomains.domain_id == domain.id).first()
                existing_unavailable_entry = session.query(UnavailableDomains).filter(UnavailableDomains.domain_id == domain.id).first()
                
                if existing_available_entry:
                    skipped_available_domains_count += 1
                    continue
                
                if existing_unavailable_entry:
                    skipped_unavailable_domains_count += 1
                    continue
                
                try:
                    response, status_code = domain_whois_check(domain_name)
                    response_data = response.get_json()
                    
                    if response_data.get('status') == 'unavailable':
                        domain_info = response_data.get('domain')
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
                        unavailable_domains_count += 1
                    elif response_data.get('status') == 'available':
                        available_domain = AvailableDomains(
                            domain_id=domain.id,
                            last_updated=datetime.now(timezone.utc)
                        )
                        session.add(available_domain)
                        available_domains_count += 1
                    else:
                        continue
                except Exception as e:
                    print(f"Error fetching WHOIS data for domain {domain_name}: {str(e)}")
            
            session.commit()
        except Exception as e:
            print(f"Error processing domains: {str(e)}")
            session.rollback()
        finally:
            session.close()
        
    return jsonify({
        'message': 'Domains processed successfully.',
        'available_domains_added': available_domains_count,
        'available_domains_skipped': skipped_available_domains_count,
        'unavailable_domains_added': unavailable_domains_count,
        'unavailable_domains_skipped': skipped_unavailable_domains_count,
    }), 200
    
# Running domain checks
def check_unavailable_domains():
    with current_app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        domains = session.query(Domains).all()
        new_available_domains = 0
        
        try:
            for domain in domains:
                domain_name = domain.domain
                
                existing_unavailable_entry = session.query(UnavailableDomains).filter(UnavailableDomains.domain_id == domain.id).first()
                
                if existing_unavailable_entry:
                    expiration_date = existing_unavailable_entry.expiration_date
                    expiration_time = existing_unavailable_entry.expiration_time
                    
                    # Combine expiration date and time into a single datetime object
                    expiration_datetime_str = f"{expiration_date} {expiration_time}"
                    expiration_datetime_naive = datetime.strptime(expiration_datetime_str, "%Y-%m-%d %H:%M:%S")
                    
                    # Make expiration_datetime timezone-aware
                    expiration_datetime = expiration_datetime_naive.replace(tzinfo=timezone.utc)
                    
                    # Get current datetime
                    current_datetime = datetime.now(timezone.utc)
                    
                    # Compare current datetime with expiration datetime
                    if current_datetime > expiration_datetime:
                        try:
                            response, status_code = domain_whois_check(domain_name)
                            response_data = response.get_json()
                            domain_info = response_data.get('domain')
                            
                            if response_data.get('status') == 'unavailable':
                                if existing_unavailable_entry:
                                    # Update the existing UnavailableDomains entry
                                    existing_unavailable_entry.creation_date = domain_info['creation_date']
                                    existing_unavailable_entry.creation_time = domain_info['creation_time']
                                    existing_unavailable_entry.expiration_date = domain_info['expiration_date']
                                    existing_unavailable_entry.expiration_time = domain_info['expiration_time']
                                    existing_unavailable_entry.name_servers = ', '.join(domain_info['name_servers']) if domain_info['name_servers'] else None
                                    existing_unavailable_entry.updated_date = domain_info['updated_date']
                                    existing_unavailable_entry.updated_time = domain_info['updated_time']
                                    existing_unavailable_entry.last_updated = datetime.now(timezone.utc)
                                else:
                                    # Create a new UnavailableDomains entry if it doesn't exist
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
                                
                                session.commit()
                            elif response_data.get('status') == 'available':
                                # Add to AvailableDomains if the domain is now available
                                available_domain = AvailableDomains(
                                    domain_id=domain.id,
                                    last_updated=datetime.now(timezone.utc)
                                )
                                session.add(available_domain)
                                new_available_domains += 1
                                session.delete(existing_unavailable_entry)
                                session.commit()
                            else:
                                continue
                        except Exception as e:
                            print(f"Error fetching WHOIS data for domain {domain_name}: {str(e)}")
                    else:
                        continue
        except Exception as e:
            print(f"Error processing unavailable domains: {str(e)}")
            session.rollback()
        finally:
            session.close()
                
    return jsonify({
        'message': 'Unavailable domain check processed successfully.',
        'available_domains_discovered': new_available_domains,
    }), 200
    
def check_available_domains():
    with current_app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        available_domains = session.query(AvailableDomains).all()
        new_unavailable_domains = 0
        
        try:
            for available_domain in available_domains:
                domain_id = available_domain.domain_id
                domain_name = session.query(Domains).filter(Domains.id == domain_id).first().domain
                
                try:
                    response, status_code = domain_whois_check(domain_name)
                    response_data = response.get_json()
                    domain_info = response_data.get('domain')
                
                    if response_data.get('status') == 'unavailable':
                        existing_unavailable_entry = session.query(UnavailableDomains).filter(UnavailableDomains.domain_id == domain_id).first()
                        
                        if existing_unavailable_entry:
                            # Update the existing UnavailableDomains entry
                            existing_unavailable_entry.creation_date = domain_info['creation_date']
                            existing_unavailable_entry.creation_time = domain_info['creation_time']
                            existing_unavailable_entry.expiration_date = domain_info['expiration_date']
                            existing_unavailable_entry.expiration_time = domain_info['expiration_time']
                            existing_unavailable_entry.name_servers = ', '.join(domain_info['name_servers']) if domain_info['name_servers'] else None
                            existing_unavailable_entry.updated_date = domain_info['updated_date']
                            existing_unavailable_entry.updated_time = domain_info['updated_time']
                            existing_unavailable_entry.last_updated = datetime.now(timezone.utc)
                        else:
                            # Create a new UnavailableDomains entry if it doesn't exist
                            unavailable_domain = UnavailableDomains(
                                domain_id=domain_id,
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
                            
                        # Remove from AvailableDomains
                        session.delete(available_domain)
                        new_unavailable_domains += 1
                        
                    session.commit()
                except Exception as e:
                    print(f"Error fetching WHOIS data for domain {domain_name}: {str(e)}")
                    session.rollback()
        except Exception as e:
            print(f"Error processing available domains: {str(e)}")
            session.rollback()
        finally:
            session.close()
                
    return jsonify({
        'message': 'Available domain check processed successfully.',
        'unavailable_domains_discovered': new_unavailable_domains,
    }), 200
    
# Getting domains
@jwt_required()
def get_available_domains():
    with current_app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        available_domains = session.query(AvailableDomains).all()
        
        result = []
        for domain in available_domains:
            result.append({
                'id': domain.id,
                'domain': domain.domain.domain,
                'moz_da': domain.moz_da,
                'moz_pa': domain.moz_pa,
                'moz_links': domain.moz_links,
                'moz_rank': domain.moz_rank,
                'moz_trust': domain.moz_trust,
                'moz_spam': domain.moz_spam,
                'stumbles': domain.stumbles,
                'pinterest_pins': domain.pinterest_pins,
                'majestic_stat': domain.majestic_stat,
                'majestic_links': domain.majestic_links,
                'majestic_ref_domains': domain.majestic_ref_domains,
                'majestic_ref_edu': domain.majestic_ref_edu,
                'majestic_ref_gov': domain.majestic_ref_gov,
                'majestic_ref_subnets': domain.majestic_ref_subnets,
                'majestic_ips': domain.majestic_ips,
                'majestic_cf': domain.majestic_cf,
                'majestic_tf': domain.majestic_tf,
                'majestic_ttf0_name': domain.majestic_ttf0_name,
                'majestic_ttf0_value': domain.majestic_ttf0_value,
                'majestic_ttf1_name': domain.majestic_ttf1_name,
                'majestic_ttf1_value': domain.majestic_ttf1_value,
                'majestic_ttf2_name': domain.majestic_ttf2_name,
                'majestic_ttf2_value': domain.majestic_ttf2_value,
                'fb_comments': domain.fb_comments,
                'fb_shares': domain.fb_shares,
                'last_updated': domain.last_updated.isoformat()
            })
        
        session.close()
        
    return jsonify(result), 200

@jwt_required()
def get_unavailable_domains():
    with current_app.app_context():
        Session = sessionmaker(bind=db.engine)
        session = Session()
        
        unavailable_domains = session.query(UnavailableDomains).all()
        
        result = []
        for domain in unavailable_domains:
            result.append({
                'id': domain.id,
                'domain': domain.domain.domain,
                'creation_date': domain.creation_date,
                'creation_time': domain.creation_time,
                'expiration_date': domain.expiration_date,
                'expiration_time': domain.expiration_time,
                'name_servers': domain.name_servers,
                'updated_date': domain.updated_date,
                'updated_time': domain.updated_time,
                'last_updated': domain.last_updated.isoformat()
            })
        
        session.close()
        
    return jsonify(result), 200