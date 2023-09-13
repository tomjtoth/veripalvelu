from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    result = db.session.execute(text("""
    SELECT *
    FROM users
    WHERE uname=:un
    """), {"un":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.passw, password):

            user = user._asdict()
            # the hashed pw should not be sent back to the client
            del user['passw']
            session["user"] = user
            return True
        else:
            return False

def logout():
    del session["user"]

def register(username, password, firstnames, lastnames, booleans):
    hash_value = generate_password_hash(password)
    try:
        db.session.execute(text("""
        INSERT INTO users(uname, passw, fnames, lnames, booleans) 
        VALUES (:un,:pw,:fn,:ln,:bool)
        """), {
            "un": username, 
            "pw": hash_value,
            "fn": firstnames,
            "ln": lastnames,
            "bool": booleans
        })
        db.session.commit()
    except:
        return False
    return login(username, password)
