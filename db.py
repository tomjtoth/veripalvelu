from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from app import app

db = SQLAlchemy(app)

# create the schema
with app.app_context():
    file_schema = open('schema.sql', 'r')
    schema = file_schema.read()
    file_schema.close()
    result = db.session.execute(text(schema))
    db.session.commit()
