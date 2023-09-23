from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from app import app, generate_random_data
from random import choice, uniform, shuffle
import threading

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

# below starts the fake population thingy

def gen_rand_gender(names_female, names_male, names_last):
    if round(uniform(0, 1)) == 0:
        return choice(names_female), choice(names_last), round(uniform(0,7))
    return choice(names_male), choice(names_last), round(uniform(8,15))



def registration_faker(i, arr, names_female, names_male, names_last):
    """
    generate fake entries string on separate threads
    """
    entries = []

    for j in range(100):
        fnames, lnames, bools = gen_rand_gender(names_female, names_male, names_last)

        entries.append(f"('_fake{i*100+j:03d}','','{fnames}','{lnames}',{bools})")

    arr[i] = ",\n".join(entries)
    
if generate_random_data:
    with app.app_context():
        # populate only once
        if int(db.session.execute(text("select count(*) from users")).fetchone()[0]) < 1000:
            print("populating users with fake data")

           
            sql_from_multithread = [None] * 10

            # below 3 name files from Wikipedia:
            names_female = [x.strip() for x in open("fake_data/names_female.lst", "r").readlines()]
            names_male = [x.strip() for x in open("fake_data/names_male.lst", "r").readlines()]
            names_last = [x.strip() for x in open("fake_data/names_last.lst", "r").readlines()]

            shuffle(names_female)
            shuffle(names_male)
            shuffle(names_last)
           
            threads = []
            for i in range(10):
                threads.append(threading.Thread(target=registration_faker, args=(i, sql_from_multithread, names_female, names_male, names_last)))
                threads[-1].start()

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into users(uname, passw, fnames, lnames, booleans) values\n"
                + ",\n".join(sql_from_multithread)
            ))
            db.session.commit()

            print("\tDONE")
