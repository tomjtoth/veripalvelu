"""Consumables related functionalities
"""

from random import choices, randint
import threading
from textwrap import dedent
from sqlalchemy.sql import text
from db import db
from app import app, generate_random_data


def get_all() -> list:
    """fetches all consumables along with their ids

    Returns:
        list: tuples of (id, name)
    """
    return db.session.execute(text("SELECT id, consumable FROM consumables")).fetchall()


def consumption_faker(
    thread_idx: int,
    arr: list[str],
    d_ids: list[int],
    c_ids: list[int]
):
    """worker thread calls this function during population of fake data

    Args:
        thread_idx (int): index of thread
        arr (list[str]): array that joins results from threads
        d_ids (list[int]): random donation ids
        c_ids (list[int]): random consumable ids
    """
    entries = []

    for donation_id in choices(d_ids, k=100):
        for consumable_id in choices(c_ids, k=randint(2, 8)):
            entries.append(f"({donation_id},{consumable_id},{randint(1,5)})")

    arr[thread_idx] = ",\n".join(entries)


with app.app_context():

    # populate necessary data once
    if db.session.execute(text("select count(*) from consumables")).scalar_one() == 0:
        db.session.execute(text(
            "insert into consumables(consumable) values\n"
            + ",\n".join([

                f"('{x.strip()}')"

                for x in dedent(
                    """\
                    alkoholiton kalja
                    kokis
                    energiajuoma
                    kahvi mustana
                    cappucino
                    appelsiinimehu
                    multivitaminmehu
                    Elovena keksi
                    makea pulla
                    kalkkunasämpylä
                    kanasämpylä
                    Marionetti karkki"""
                ).splitlines()
            ])
        ))
        db.session.commit()

    if generate_random_data:
        if db.session.execute(text("select count(*) from consumption")).scalar_one() < 100:
            print("populating consuption with fake data")

            consumable_ids = [
                x[0]
                for x in db.session.execute(text("select id from consumables")).fetchall()
            ]

            donation_ids = [
                x[0]
                for x in db.session.execute(text("select id from donations")).fetchall()
            ]

            sql_from_multithread = [None] * 10

            threads = []
            for i in range(9):
                threads.append(threading.Thread(target=consumption_faker, args=(
                    i, sql_from_multithread, donation_ids, consumable_ids)))
                threads[-1].start()

            # do the last part on the main thread
            consumption_faker(9, sql_from_multithread,
                              donation_ids, consumable_ids)

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into consumption(donation_id, consumable_id, consumed_qty) values\n"
                + ",\n".join(sql_from_multithread)
            ))
            db.session.commit()
            print("\tDONE")
