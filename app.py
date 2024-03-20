"""## main module

responsible for:
- reading in command line arguments
"""

from os import getenv
from flask import Flask


app = Flask(__name__)
app.secret_key = getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

# autopep8 wants this on the top...
# fmt: off
import routes # pylint: disable=wrong-import-position,unused-import
