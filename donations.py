from db import db
from flask import session
from sqlalchemy.sql import text
import math
from app import app, generate_random_data
from random import randint, random, choice, choices, shuffle
import time
from datetime import date, timedelta
import threading
import plotly
import plotly.graph_objs as go
import json


def register(date: str, clinic_id: int, consumption, comment: str):
    consumable = 0

    # set 1 bit at a time
    for c in consumption:
        consumable |= int(math.pow(2, c))

    try:
        db.session.execute(text("""
        insert into donations(user_id, clinic_id, ddate)
        values(:uid, :cid, :dd)"""), {
            'uid': session['user']['id'],
            'cid': clinic_id,
            'dd': date
        })
        if consumable > 0:
            db.session.execute(text("""
            insert into consumption(donation_id, consumed)
            select currval(pg_get_serial_sequence('donations','id')), :x
            """), {'x': consumable})
        if comment != "":
            db.session.execute(text("""
            insert into comments(donation_id, comment)
            select currval(pg_get_serial_sequence('donations','id')), :x
            """), {'x': comment})

        db.session.commit()

    except:
        return False

    return True


def plot(user_id=None, crit="clinic"):

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

    return (
        json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps({
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
            'title': f"""{
                'Luovutuspaikkojen' 
                if crit == 'clinic' 
                else 'Veriryhmien'
            } perusteella""",
            'font': {
                'color': 'red'
            },
            'plot_bgcolor': 'transparent',
            'paper_bgcolor': 'transparent',
        }, cls=plotly.utils.PlotlyJSONEncoder)
    ) if len(data) > 0 else None


def rand_date():
    fmt = "%Y-%m-%d"
    stime = time.mktime(time.strptime("2000-01-01", fmt))
    etime = time.mktime(time.strptime(date.today().strftime(fmt), fmt))

    ptime = stime + random() * (etime - stime)

    return time.strftime(fmt, time.localtime(ptime))


    """generate fake entries string on separate threads
    """
    entries = []

    for _ in range(1000):
        entries.append(
            f"({choice(user_ids)},{choice(clinic_ids)},'{rand_date()}')")

    arr[i] = ",\n".join(entries)


    """generate fake entries string on separate threads
    """
    entries = []

    for id in choices(donation_ids, k=100):
        entries.append(f"({id},'{choice(comments)}')")

    arr[i] = ",\n".join(entries)


def all_comments():
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
        if db.session.execute(text("select count(*) from donations")).scalar_one() < 10:
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
            for i in range(10):
                threads.append(threading.Thread(target=donation_faker, args=(
                    i, sql_from_multithread, user_ids, clinic_ids)))
                threads[-1].start()

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into donations(user_id, clinic_id, ddate) values\n"
                + ",\n".join(sql_from_multithread)
            ))

            # comments from ChatGPT: "generate 50 random comments about how good it was to donate blood in Finnish"
            comments = [
                x.strip().replace("'", "''")
                for x in open("fake_data/comments.lst", "r").readlines()
            ]

            shuffle(comments)

            donation_ids = [
                x[0]
                for x in db.session.execute(text("select id from donations")).fetchall()
            ]

            threads = []
            for i in range(10):
                threads.append(threading.Thread(target=comment_faker, args=(
                    i, sql_from_multithread, donation_ids, comments)))
                threads[-1].start()

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into comments(donation_id, comment) values\n"
                + ",\n".join(sql_from_multithread)
            ))

            db.session.commit()
            print("\tDONE")
