"""## main module

responsible for:
- reading in command line arguments
- creating the `.env` preset
"""

from os import getenv, path, environ
import secrets
from subprocess import CalledProcessError, run
import sys
from textwrap import dedent
import uuid
from flask import Flask

if getenv("CREATE_DOTENV", "false") == "true":
    POSTGRES_PASSWORD = str(uuid.uuid4())
    with open(".env", "a", encoding="utf8") as f:
        f.write(dedent(f"""
        # needed for Flask
        SERCET_KEY={str(uuid.uuid4())}
        
        # needed for docker-compose, too
        POSTGRES_PASSWORD={POSTGRES_PASSWORD}
        
        # this might need to be adjusted
        DATABASE_URL=postgresql+psycopg2://vp:{POSTGRES_PASSWORD}@localhost/vp
        """))
    sys.exit()


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

# autopep8 wants this on the top...
# fmt: off
import routes # pylint: disable=wrong-import-position,unused-import
