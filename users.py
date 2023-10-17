"""Manages users related functionalities
"""

import secrets
from random import choice, choices, uniform, shuffle
import threading
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2 import OperationalError
from db import db
from app import app, generate_random_data


def login(username: str, password: str) -> bool:
    """tries to log the user in, setting session["user"] upon success

    Returns:
        bool: describing whether the process succeeded or not
    """

    result = db.session.execute(text("""
    SELECT id, uname, passw, fnames, blood_type(flags)
    FROM users
    WHERE uname=:un
    """), {"un": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.passw, password):

            user = user._asdict()
            # the hashed pw should not be sent back to the client
            del user['passw']
            user['csrf'] = secrets.token_hex(16)
            session["user"] = user
            return True
        else:
            return False


def logout():
    """simply deletes session["user"]
    """

    del session["user"]


def register(username: str, password: str, firstnames: str, lastnames: str, flags: int) -> bool:
    """tries to register the user
    """
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
    except OperationalError:
        return False
    return login(username, password)


all_blood_types = '0- 0+ A- A+ B- B+ AB- AB+'.split(' ')


def flags_from_form(is_male: bool, blood_type: int, is_admin: bool = False) -> int:
    """resolves the flags from the form

    Args:
        is_male (bool): user's sex
        blood_type (int): user's blood type
        is_admin (bool, optional): admin account. Defaults to False.

    Returns:
        int: this can be stored in the DB
    """
    flags = blood_type

    if is_admin:
        flags |= 0x10000

    if is_male:
        flags |= 0x1000

    return flags

# below starts the fake population thingy


def gen_rand_gender(
        names_female: list[str],
        names_male: list[str],
        names_last: list[str]
) -> (str, str, int):
    """creates a random user

    Args:
        names_female (list[str]): list of female firstnames from Wikipedia
        names_male (list[str]): list of male firstnames from Wikipedia
        names_last (list[str]): list of lastnames from Wikipedia

    Returns:
        (str, str, int): a tuple of (firstname, lastname, flags)
    """
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


def registration_faker(
        thread_idx: int,
        arr: list[str],
        names_female: list[str],
        names_male: list[str],
        names_last: list[str]
):
    """generate fake entries string on separate threads

    Args:
        thread_idx (int): index of thread
        arr (list[str]): list in main thread to put the results into
        names_female (list[str]): list of female firstnames from Wikipedia
        names_male (list[str]): list of male firstnames from Wikipedia
        names_last (list[str]): list of lastnames from Wikipedia
    """
    entries = []

    for j in range(100):
        fnames, lnames, bools = gen_rand_gender(
            names_female, names_male, names_last
        )

        entries.append(
            f"('_fake{thread_idx*100+j:03d}','','{fnames}','{lnames}',{bools})")

    arr[thread_idx] = ",\n".join(entries)


if generate_random_data:
    with app.app_context():
        # populate only once
        if db.session.execute(text("select count(*) from users")).scalar_one() < 100:
            print("populating users with fake data")

            sql_from_multithread = [None] * 10

            # below 3 name files from Wikipedia:
            female_names = [
                x.strip() for x in open(
                    "fake_data/names_female.lst", "r", encoding='utf8'
                ).readlines()
            ]
            male_names = [
                x.strip() for x in open(
                    "fake_data/names_male.lst", "r", encoding='utf8'
                ).readlines()
            ]
            surnames = [
                x.strip() for x in open(
                    "fake_data/names_last.lst", "r", encoding='utf8'
                ).readlines()
            ]

            shuffle(female_names)
            shuffle(male_names)
            shuffle(surnames)

            threads = []
            for i in range(9):
                threads.append(threading.Thread(target=registration_faker, args=(
                    i, sql_from_multithread, female_names, male_names, surnames)))
                threads[-1].start()

            # do the last part on the main thread
            registration_faker(9, sql_from_multithread,
                               female_names, male_names, surnames)

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into users(uname, passw, fnames, lnames, flags) values\n"
                + ",\n".join(sql_from_multithread)
            ))
            db.session.commit()

            print("\tDONE")
