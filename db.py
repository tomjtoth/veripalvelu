"""Handles DB related preparations
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from psycopg2 import OperationalError
from app import app

db = SQLAlchemy(app)

# create the schema
with app.app_context():
    with open('schema.sql', 'r', encoding='utf8') as f:
        try:
            db.session.execute(text(f.read()))
            db.session.commit()

        except OperationalError:
            db.session.rollback()
