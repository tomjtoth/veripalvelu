"""### Manages donation-related functionalities
"""

from datetime import date, timedelta
import json
import time
import threading
from random import random, choice, choices, shuffle
from flask import session
from sqlalchemy.sql import text
import plotly
import plotly.graph_objs as go
from psycopg2 import OperationalError
from db import db
from app import app, generate_random_data


def register(donation_date: str, clinic_id: int, cons: list[int], comment: str):
    """registers 1 donation to the DB

    Args:
        donation_date (str): date of donation
        clinic_id (int): id of clinic the donation took place at
        consumables (list[int]): quantities of consumables
        comment (str): optional comments of donation experience
    """

    # this must be here, otherwise during population of fake data would get stuck
    import consumables  # pylint: disable=import-outside-toplevel

    try:
        donation_id = db.session.execute(text(
            """
            insert into donations(user_id, clinic_id, ddate)
            values(:uid, :cid, :dd)
            returning id
            """
        ), {
            'uid': session['user']['id'],
            'cid': clinic_id,
            'dd': donation_date
        }).scalar_one()

        consumables_sql = []

        for cons_id, cons_qty in zip([x[0] for x in consumables.get_all()], cons):
            if cons_qty > 0:
                consumables_sql.append(f"({donation_id},{cons_id},{cons_qty})")

        if len(consumables_sql) > 0:
            db.session.execute(text(
                "insert into consumption(donation_id, consumable_id, consumed_qty) values\n"
                # this should be safe as conversion to list[int] is enforced in routes.py
                + ",".join(consumables_sql)
            ))
        if comment != "":
            db.session.execute(text(
                "insert into comments(donation_id, comment) values (:id, :c)"
            ), {
                'id': donation_id,
                'c': comment
            })

        db.session.commit()

    except OperationalError:
        db.session.rollback()
        return False

    return True


def plot(user_id: int = None, crit: str = "clinic") -> (str, str):
    """gets data and config for plotly charts

    Args:
        user_id (int): filtering DB query by user_id if present. Defaults to None.
        crit (str): filtering criterium. Defaults to "clinic".

    Returns:
        (str, str): a tuple of `data` + `conf` in JSON serialized form that's jinja compatible
        or None: in case there's no data
    """

    translation = {
        'clinic': 'Luovutuspaikkojen',
        'blood_type': 'Veriryhmien',
        'sex': 'Sukupuolten'
    }

    data = [

        go.Bar(
            name=name,
            x=x,
            y=y,
            hoverinfo="x+name+y",
            showlegend=True
        )

        for name, x, y in db.session.execute(text(f"""
            with cte as (
                select 
                    __CRIT__, 
                    date, 
                    count(*)
                from data
                {"where user_id = " + str(user_id) if user_id else ""}
                group by __CRIT__, date
                order by __CRIT__
            )
            select
                __CRIT__,
                json_agg(date),
                json_agg(count)
            from cte
            group by __CRIT__
            order by __CRIT__;
            """.replace("__CRIT__", crit)
        )).fetchall()
    ]

    return {
        'name': crit,

        'data': json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder),

        'conf': json.dumps({
            'barmode': "relative",
            'scrollZoom': True,
            'xaxis': {
                'range': [
                    date.today() - timedelta(weeks=4*3),
                    # today's donations were only visible half-width :D
                    date.today() + timedelta(days=1)
                ],
                'title': "päivämäärä"
            },
            'yaxis': {'title': "luovutukset"},
            'title': f"{translation[crit]} perusteella",
            'font': {
                'color': 'red'
            },
            'plot_bgcolor': 'transparent',
            'paper_bgcolor': 'transparent',
        }, cls=plotly.utils.PlotlyJSONEncoder)
    } if len(data) > 0 else None


def rand_date(start_date: str = "2000-01-01") -> str:
    """picks a random date between min and today

    Args:
        start_date (str): datestring in the form of "YYYY-MM-DD"

    Returns:
        str: a random date in the form of "YYYY-MM-DD"
    """
    fmt = "%Y-%m-%d"
    stime = time.mktime(time.strptime(start_date, fmt))
    etime = time.mktime(time.strptime(date.today().strftime(fmt), fmt))

    ptime = stime + random() * (etime - stime)

    return time.strftime(fmt, time.localtime(ptime))


def donation_faker(thread_idx: int, arr: list[str], u_ids: list[int], c_ids: list[int]):
    """generate fake entries string on separate threads

    Args:
        thread_idx (int): index of thread
        arr (list[str]): list to insert the results into
        u_ids (list[int]): user ids to randomly pick from
        c_ids (list[int]): clinic ids to randomly pick from
    """
    entries = []

    for _ in range(1000):
        entries.append(
            f"({choice(u_ids)},{choice(c_ids)},'{rand_date()}')")

    arr[thread_idx] = ",\n".join(entries)


def comment_faker(thread_idx: int, arr: list[str], d_ids: list[int], comments: list[str]):
    """generate fake entries string on separate threads

    Args:
        thread_idx (int): index of thread
        arr (list[str]): list to insert the results into
        d_ids (list[int]): all donation ids
        comments (list[str]): all comments
    """
    entries = []

    for donation_id in choices(d_ids, k=100):
        entries.append(f"({donation_id},'{choice(comments)}')")

    arr[thread_idx] = ",\n".join(entries)


def get_all_comments() -> list:
    """get all comments from DB
    """
    return [

        row[0] for row in

        db.session.execute(text("""
            select json_build_object(
                'd', date,
                'cl', clinic,
                'fn', substring(fnames, 1, 1),
                'ln', substring(lnames, 1, 1),
                'qt', comment
            )
            from data
            where comment is not null
        """)).fetchall()
    ]


if generate_random_data:
    with app.app_context():
        # populate only once
        if db.session.execute(text("select count(*) from donations")).scalar_one() < 100:
            print("populating donations with fake data")

            clinic_ids = [
                x[0]
                for x in db.session.execute(text("select id from clinics")).fetchall()
            ]

            user_ids = [
                x[0]
                for x in db.session.execute(text("select id from users")).fetchall()
            ]

            sql_from_multithread = [None] * 10

            threads = []
            for i in range(9):
                threads.append(threading.Thread(target=donation_faker, args=(
                    i, sql_from_multithread, user_ids, clinic_ids)))
                threads[-1].start()

            # do the last part on the main thread
            donation_faker(9, sql_from_multithread, user_ids, clinic_ids)

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into donations(user_id, clinic_id, ddate) values\n"
                + ",\n".join(sql_from_multithread)
            ))

            # comments from ChatGPT
            with open("fake_data/comments.lst", "r", encoding='utf8') as f:
                all_comments = [
                    x.strip().replace("'", "''")
                    for x in f.readlines()
                ]

            shuffle(all_comments)

            donation_ids = [
                x[0]
                for x in db.session.execute(text("select id from donations")).fetchall()
            ]

            threads = []
            for i in range(9):
                threads.append(threading.Thread(target=comment_faker, args=(
                    i, sql_from_multithread, donation_ids, all_comments)))
                threads[-1].start()

            # do the last part on the main thread
            comment_faker(9, sql_from_multithread, donation_ids, all_comments)

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into comments(donation_id, comment) values\n"
                + ",\n".join(sql_from_multithread)
            ))

            db.session.commit()
            print("\tDONE")
