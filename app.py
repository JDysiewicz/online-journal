import os

import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
from datetime import datetime
from datetime import date
from datetime import time

# Configure application
app = Flask(__name__)

# table of users already exists - users(id, name, hash)
# Find replace sqlite parts

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
    return render_template("index.html", date = datetime.now())

@app.route("/previous", methods=["GET", "POST"])
def previous():
    if request.method == "GET":
        conn = sqlite3.connect("submissions.db")
        db = conn.cursor()
        entries = list(db.execute("SELECT entry FROM entries WHERE id = :id", {"id":session["user_id"]}))
        if not entries:
            return render_template("temp.html", message="No entries")
        dates = list(db.execute("SELECT date FROM entries WHERE id = :id", {"id":session["user_id"]}))
        postid = list(db.execute("SELECT postid FROM entries WHERE id = :id", {"id":session["user_id"]}))
        conn.commit()
        conn.close
        return render_template("previous.html", entrydate = zip(entries,dates,postid))
    else:
        return redirect("/")


@app.route("/delete-entry", methods=["POST"])
def delete_entry():
    conn = sqlite3.connect("submissions.db")
    db = conn.cursor()
    db.execute("DELETE FROM entries WHERE postid = :postid", {"postid": request.form['delete']})
    conn.commit()
    conn.close()
    return redirect("/previous")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # initiate connection with database
        conn = sqlite3.connect("project.db")
        db = conn.cursor()

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = list(db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": request.form.get("username")}))
        if not rows:
            return apology("Invalid Username and/or Password", 403)
        # Ensure password is correct
        if not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page and close connection to database
        conn.close()
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/write",methods=["GET", "POST"])
def write():
    if request.method == "POST":
        conn = sqlite3.connect("submissions.db")
        db = conn.cursor()
        print(session["user_id"])
        if request.form.get("entry"):
            db.execute("INSERT INTO entries(id, entry, date, time) VALUES(:id, :entry, :date, :time)", {"id": session["user_id"], "entry": request.form.get("entry"), "date": date.today(), "time": datetime.now()})
            conn.commit()
            
        conn.close
        return redirect("/")

    else:
        return render_template("write.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    """Register User"""
    if request.method == "POST":
        conn = sqlite3.connect("project.db")
        db = conn.cursor()

        # error checking
        if not request.form.get("username"):
            return apology("No Username", 400)

        elif not request.form.get("password"):
            return apology("No password", 400)

        elif not request.form.get("confirmation"):
            return apology("Please confirm your password", 400)

        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("Passwords do not match", 400)

        username = request.form.get("username")

        # encrypt password
        hash = generate_password_hash(request.form.get("password"))

        taken = list(db.execute("SELECT username FROM users WHERE username = :username", {"username": username}))
        print(taken)
        if taken != []:
            return apology("Sorry, that username is already taken")
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)", {"username": username, "hash": hash})
        conn.commit()
        result = list(db.execute("SELECT id FROM users WHERE username = :username AND hash = :hash", {"username": username, "hash": hash}))
        session["user_id"] = result
        print (session["user_id"])
        conn.close()
        return redirect("/login")
    else:
        return render_template("register.html")



# Change Password Tab
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        if not (request.form.get("password")) or not request.form.get("password-conf"):
            return apology("Please enter your desired new password")
        if request.form.get("password") != request.form.get("password-conf"):
            return apology("Your passwords did not match, please try again")

        hash = generate_password_hash(request.form.get("password"))
        db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=hash, id=session["user_id"])
        return redirect("/")

    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

app.run(host='127.0.0.1', port= 80)