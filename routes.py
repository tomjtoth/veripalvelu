"""Manages what happens on what path
"""

from datetime import date
import re
from flask import json, render_template, redirect, request, session, abort
from markupsafe import escape
from app import app, force_https
import users
import clinics
import donations
import consumables

# checking name lengths is taken care of here, too
re_names = re.compile(r"^(.{1,100}) *(?:,|<PILKKU>) *(.{1,100})$")
re_linefeed = re.compile(r"\r?\n")


def valid_date(date_text: str) -> bool:
    """checks if a date is valid AND smaller than today

    Args:
        date_text (str): date to be checked in the format of "YYYY-MM-DD"
    """
    try:
        if date.today() < date.fromisoformat(date_text):
            return False
        return True
    except ValueError:
        return False

# this is not working as flask won't run on both http and https
# @app.before_request


def before_request():
    """WiP - this was supposed to redirect HTTP -> HTTPS in production
    """
    if force_https and not request.is_secure:
        return redirect(
            request.url.replace('http://', 'https://', 1),
            code=301
        )


@app.route("/register", methods=["GET", "POST"])
def register():
    """handles registering the user
    """
    if request.method == "GET":
        return render_template("register.html",
                               blood_types=users.all_blood_types)
    if request.method == "POST":
        password = request.form["password"]
        if password != request.form["pw-verify"]:
            return render_template("error.html", err="Salasanat eroavat", retry='register')

        if len(password) < 8:
            return render_template("error.html", err="liian lyhyt salasana", retry='register')

        names = re_names.match(request.form["names"])

        if not names:
            return render_template("error.html", err="nimet väärin", retry='register')

        if users.register(
            request.form["username"],
            password,
            names.group(2),
            names.group(1),
            users.flags_from_form(
                int(request.form["gender"]) == 1,
                int(request.form["blood-type"])
            )
        ):
            return redirect("/")

        return render_template(
            "error.html",
            operation='rekisteröinti',
            err="Käyttäjätunnus varmaan otettu jo",
            retry='register')


@app.route("/login", methods=["GET", "POST"])
def login():
    """handles logging the user in
    """
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")

        return render_template(
            "error.html",
            operation='kirjautuminen',
            err="Väärä tunnus tai salasana",
            retry='login')


@app.route("/logout")
def logout():
    """handles logging the user out
    """
    users.logout()
    return redirect("/")


@app.route('/')
def root():
    """shows the basic view
    """
    return render_template(
        'index.html',
        plots=[
            donations.plot(),
            donations.plot(crit="blood_type"),
            donations.plot(crit="sex"),

            donations.plot(session.get('user')['id'])
            if session.get('user') else None
        ]
    )


@app.route('/donate', methods=["GET", "POST"])
def donate():
    """handles registering a donation
    """
    if not session.get('user'):
        return redirect('/login')

    if request.method == "GET":
        return render_template(
            'donation.html',
            clinics=clinics.get_names(),
            today=date.today(),
            consumables=consumables.get_all()
        )

    # we don't even have a session yet
    if not session.get("user"):
        return redirect("/login")

    # or CSRF mismathed
    if request.form.get("csrf") is None or request.form["csrf"] != session["user"]["csrf"]:
        abort(403)

    comment = request.form['comment']

    if len(comment) > 5000:
        return render_template("error.html", err="liian pitkä kommentti", retry='donate')

    donation_date = request.form['date']
    if not valid_date(donation_date):
        return render_template("error.html", err="päivämäärä tulevaisuudessa", retry='donate')

    if donations.register(
        donation_date,
        request.form['clinic'],
        request.form.getlist('consumables', int),
        re_linefeed.sub('<br/>', str(escape(comment)))
    ):
        return redirect('/')

    return render_template('error.html', err='emt', retry='donate')


@app.route('/comments')
def comments():
    """rendering all comments
    """
    return render_template('comments.html', comments=donations.get_all_comments())


@app.route('/api/heartbeat')
def heartbeat():
    """retrieving number of registered donations via REST API (?)

    Returns:
        int: count of registered donations
    """
    return json.jsonify(donations.get_total_count())
