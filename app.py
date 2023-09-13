from flask import Flask
from os import getenv, path
import secrets

# create default .env if not exists
if not path.exists('.env'):
    f = open('.env', 'w')
    f.write(f"""# modify these to your liking
DATABASE_URL=postgresql:///user
SECRET_KEY={secrets.token_hex(16)}
""")
    f.close()
    print('\n\tcreated sample config file as .env\n\trevise it, then restart the app\n')
    exit(0)


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

import routes
