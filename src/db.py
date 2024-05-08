"""Handles DB related preparations
"""

from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)
