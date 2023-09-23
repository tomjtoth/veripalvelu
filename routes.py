from flask import send_from_directory, render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
import users, clinics, donations, consumables
import re

re_names = re.compile(r"(.+), *(.+)")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", 
            blood_types='0+,0-,A+,A-,B+,B-,AB+,AB-'.split(','))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        pw_verify = request.form["pw-verify"]
        if password != pw_verify:
            return render_template("error.html", err="Salasanat eroavat")

        names = re_names.match(request.form["names"])

        if not (names):
            return render_template("error.html", err="nimet väärin")

        booleans = 0x0

        # admin is the leftmost bit, never used atm
        if False:
            booleans |= 0x10000
        
        if int(request.form["gender"]) == 1:
            booleans |= 0x1000
        
        blood_type = int(request.form["blood-type"])
        
        # type A
        if blood_type in (2,3,6,7):
            booleans |= 0x100

        # type B
        if blood_type in (4,5,6,7):
            booleans |= 0x10

        # RH +
        if blood_type in (0,2,4,6):
            booleans |= 0x1

        if users.register(
            username, 
            password, 
            names.group(2), 
            names.group(1), 
            booleans):
            return redirect("/")
        else:
            return render_template(
                "error.html",
                operation='rekisteröinti',
                err="Käyttäjätunnus varmaan otettu jo")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template(
                "error.html", 
                operation='kirjautuminen',
                err="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    del session["user"]
    return redirect("/")

@app.route('/')
def root():
    return render_template('index.html')
