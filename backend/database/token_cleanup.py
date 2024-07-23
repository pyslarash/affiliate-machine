from flask import Flask
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import scoped_session, sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(automatic_remove_token, 'interval', hours=1, id='token_cleanup_job')
    scheduler.start()
    app.logger.info("Scheduler started, cleaning up expired tokens every hour.")

def remove_token(token):
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)
    session = Session()
    try:
        from database.models import TokenBlacklist
        blacklisted_token = session.query(TokenBlacklist).filter_by(token=token).first()
        if not blacklisted_token:
            return 'Token not found in blacklist', 404

        session.delete(blacklisted_token)
        session.commit()
        return 'Token removed from blacklist successfully', 200
    except Exception as e:
        session.rollback()
        return str(e), 500
    finally:
        session.close()

def automatic_remove_token():
    with app.app_context():
        expiration_time = datetime.now(timezone.utc) - timedelta(hours=24)
        from database.models import TokenBlacklist
        expired_tokens = TokenBlacklist.query.filter(TokenBlacklist.created_at < expiration_time).all()
        for token_record in expired_tokens:
            remove_token_response, status_code = remove_token(token_record.token)
            if status_code != 200:
                print(f"Error removing token {token_record.token}: {remove_token_response}")
            else:
                print(f"Token {token_record.token} removed successfully.")

if __name__ == '__main__':
    with app.app_context():
        token_to_delete = input("Please enter the token to delete from the blacklist: ")
        response, status_code = remove_token(token_to_delete)
        print(response)
