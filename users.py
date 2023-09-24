from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from app import app, generate_random_data
from random import choice, choices, uniform, shuffle
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

def register(username, password, firstnames, lastnames, flags):
    hash_value = generate_password_hash(password)
    try:
        db.session.execute(text("""
        INSERT INTO users(uname, passw, fnames, lnames, flags) 
        VALUES (:un,:pw,:fn,:ln,:flags)
        """), {
            "un": username,
            "pw": hash_value,
            "fn": firstnames,
            "ln": lastnames,
            "flags": flags
        })
        db.session.commit()
    except:
        return False
    return login(username, password)

all_blood_types = '0- 0+ A- A+ B- B+ AB- AB+'.split(' ')

def flags_from_form(is_male, blood_type, is_admin = False):
    flags = blood_type

    if is_admin:
        flags |= 0x10000
    
    if is_male:
        flags |= 0x1000

    return flags

# below starts the fake population thingy

def gen_rand_gender(names_female, names_male, names_last):
    [flags] = choices(

        # 1st 3 bits of the flags are A,B,RH
        range(8),

        # returning only one
        k=1,

        # from https://www.blood.co.uk/why-give-blood/blood-types/
        weights=(35, 13, 30, 8, 8, 2, 2, 1)
    )
    if round(uniform(0, 1)) == 0:
        fnames = names_female
    else:
        fnames = names_male
        flags |= 0x1000
    return choice(fnames), choice(names_last), flags



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
                "insert into users(uname, passw, fnames, lnames, flags) values\n"
                + ",\n".join(sql_from_multithread)
            ))
            db.session.commit()

            print("\tDONE")
