"""Handles DB related preparations
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from app import app

db = SQLAlchemy(app)

# create the schema
with app.app_context():
    with open('schema.sql', 'r', encoding='utf8') as f:
        try:
            db.session.execute(text(f.read()))
            db.session.commit()

        # pylint: disable=bare-except
        except:
            db.session.rollback()
