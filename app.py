"""## main module

responsible for:
- reading in command line arguments
- creating the `.env` preset
- creating a randomized database 
"""

from os import getenv, path, environ
import secrets
from subprocess import CalledProcessError, run
import sys
import uuid
from flask import Flask

# create .env preset if not exists
if not path.exists('.env'):
    db_name = f"verenluovutus-{uuid.uuid4()}"
    DB_NAME = """\
# the below database has been automatically created
DATABASE_URL=postgresql:///{db_name}"""

    with open('.env', 'w', encoding='utf8') as f:
        try:
            run(["createdb", db_name], check=True)
            print("""\
\t`./.env` was missing, generated from presets
\treview it and restart the program\n
""")

        except CalledProcessError:
            print("\n\tfollow the instructions in the newly created `./.env` file\n")
            DB_NAME = """\
# automatic database creation failed ¯\\_(ツ)_/¯
# run `createdb verenluovutus-sovellus` however you see fit
# schema.sql gets loaded automatically, no worries there!
# modify the below line if necessary
DATABASE_URL=postgresql:///verenluovutus-sovellus"""

        finally:
            f.write(f"""\
{DB_NAME}

# Flask related
SECRET_KEY={secrets.token_hex(16)}

# populate the database with fake users, donations, comments, consumptions
# this is really advised as charts would be quite boring to look at without it
GEN_RAND_DATA=true

# the below part is only required in the production environment
# HOST=0.0.0.0
# PORT=xxxxx
# TLS_CERT=/path/to/fullchain.pem
# TLS_KEY=/path/to/privkey.pem
""")
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
