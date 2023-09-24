from flask import Flask
from os import getenv, path, environ
import secrets, uuid
from subprocess import run

# create default .env if not exists
if not path.exists('.env'):
    db_name = f"verenluovutus-{uuid.uuid4()}".replace("-", "_")
    f = open('.env', 'w')
    f.write(f"""
# the below database has already been created for the app
# remember to `createdb YOUR_DB` if you modify the below string to
# DATABASE_URL=postgresql:///YOUR_DB
DATABASE_URL=postgresql:///{db_name}
SECRET_KEY={secrets.token_hex(16)}
GEN_RAND_DATA=true
""")
    f.close()
    try:
        run(["createdb", db_name])
        print('\n\t./.env missing, generated from presets\n\tnow restart the program\n')
        RC=0
    except:
        print(f'\n\tfailed to create database: "{db_name}"')
        RC=1
    finally:
        exit(RC)

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
generate_random_data = environ.get("GEN_RAND_DATA", "false") == "true"

import routes
