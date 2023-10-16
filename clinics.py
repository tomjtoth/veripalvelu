from db import db
from flask import session
from sqlalchemy.sql import text
from app import app


def get_names():
    return tuple(db.session.execute(text('select id, cname from clinics')).fetchall())


with app.app_context():
    if db.session.execute(text("select count(*) from clinics")).scalar_one() == 0:
        db.session.execute(text(
            "insert into clinics(cname) values\n" +
            ",".join([

                f"('{x.strip()}')"

                for x in """
                    Espoo, Iso Omena
                    Helsinki, Kivihaka
                    Helsinki, Sanomatalo
                    Jyväskylä
                    Kuopio
                    Lahti, Kauppakeskus Trio
                    Oulu
                    Seinäjoki
                    Tampere
                    Turku
                """.splitlines() if x.strip() != ""
            ])))
        db.session.commit()
