from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask import current_app as app

def create_db():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created")
    else:
        print("Database already exists")
    engine.dispose()