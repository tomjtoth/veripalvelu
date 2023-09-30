from db import db
from sqlalchemy.sql import text
from app import app, generate_random_data
from random import choices, choice, randint
import threading

def get_all():
    return db.session.execute(text("SELECT id, consumable FROM consumables")).fetchall()

def consumption_faker(i, arr, donation_ids, consumable_ids):
    """
    generate fake entries string on separate threads
    """
    entries = []
    
    for donation_id in choices(donation_ids, k=100):
        for consumable_id in choices(consumable_ids, k=randint(2,8)):
            entries.append(f"({donation_id},{consumable_id})")

    arr[i] = ",\n".join(entries)
    
with app.app_context():
    
    # populate necessary data once
    if int(db.session.execute(text("select count(*) from consumables")).fetchone()[0]) == 0:
        db.session.execute(text(
            "insert into consumables(consumable) values\n"
            + ",\n".join([ f"('{x.strip()}')"
                for x in 
                """alkoholiton kalja
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
                Marionetti karkki""".splitlines()
            ])
        ))
        db.session.commit()
        
    if generate_random_data:
        if int(db.session.execute(text("select count(*) from consumption")).fetchone()[0]) < 10000:
            print("populating consuption with fake data")
            
            consumable_ids = [x[0]
                for x in db.session.execute(text("select id from consumables")).fetchall()
            ]

            donation_ids = [x[0]
                for x in db.session.execute(text("select id from donations")).fetchall()
            ]

            sql_from_multithread = [None] * 10

            threads = []
            for i in range(10):
                threads.append(threading.Thread(target=consumption_faker, args=(i, sql_from_multithread, donation_ids, consumable_ids)))
                threads[-1].start()

            # wait for the threads to complete
            for t in threads:
                t.join()

            db.session.execute(text(
                "insert into consumption(donation_id, consumable_id) values\n"
                + ",\n".join(sql_from_multithread)
            ))
            db.session.commit()
            print("\tDONE")

