import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from database import db, migrate
from database.create_db import create_db
from config import Config
from api import *

app = Flask(__name__)
CORS(app)  # Enable CORS for all route
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
migrate.init_app(app, db)

# Initialize the JWT manager
jwt = JWTManager(app)

with app.app_context():
    from database.models import *
    create_db()

# Deferred import to avoid circular import
def init_scheduler():
    from database.token_cleanup import init_scheduler as scheduler_init
    scheduler_init(app)

if __name__ == '__main__':
    init_scheduler()
    user_routes(app)
    jan_ai(app)
    api_keys(app)
    czds(app)
    app.run()