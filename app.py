"""## main module

responsible for:
- reading in command line arguments
- creating the `.env` preset
- creating a randomized database 
"""

from os import getenv, path, environ
import secrets
from subprocess import run
import sys
import uuid
from flask import Flask

# create default .env if not exists
if not path.exists('.env'):
    db_name = f"verenluovutus-{uuid.uuid4()}".replace("-", "_")
    with open('.env', 'w', encoding='utf8') as f:
        try:
            run(["createdb", db_name], check=False)
            print(
                '\n\t./.env missing, generated from presets\n\tnow restart the program\n')
            f.write(f"""\
# the below database has already been created for the app
# remember to `createdb YOUR_DB` if you modify the below string to
# DATABASE_URL=postgresql:///YOUR_DB
DATABASE_URL=postgresql:///{db_name}
SECRET_KEY={secrets.token_hex(16)}
GEN_RAND_DATA=true

# the below is only present because of the VPS
HOST=0.0.0.0
PORT=xxxxx
""")
        # pylint: disable=bare-except
        except:
            print(f'\n\tfailed to create database: "{db_name}"')
        finally:
            sys.exit()


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
generate_random_data = environ.get("GEN_RAND_DATA", "false") == "true"

force_https = next((
    True
    for arg in sys.argv
    if arg.startswith("--cert=")
    or arg.startswith("--key=")
), False)

# autopep8 wants this on the top...
# fmt: off
import routes # pylint: disable=wrong-import-position,unused-import
