"""## main module

responsible for:
- reading in command line arguments
"""

from os import getenv
import sys
from flask import Flask

GEN_RAND_DATA = getenv("GEN_RAND_DATA")

app = Flask(__name__)
app.secret_key = getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

# autopep8 wants this on the top...
# fmt: off
import routes # pylint: disable=wrong-import-position,unused-import

if GEN_RAND_DATA:
    sys.exit()
