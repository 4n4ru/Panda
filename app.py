import os
from flask import (Flask, render_template,
                   request, redirect,
                   session, flash,
                   url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/companies')
def companies():
    companies = mongo.db.companies.find()
    return render_template("companies.html", companies=companies)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # Check if a username exists
    if request.method == "POST":
        existing_user = mongo.db.Users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username is already taken")
            return redirect(url_for('signup'))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "companyName": request.form.get("companyName").lower(),
            "companyAddress": request.form.get("companyAddress").lower(),
            "companyWebsite": request.form.get("companyWebsite").lower()
        }
        mongo.db.Users.insert_one(register)
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("sign-up.html")


@app.route('/createProfile', methods=["GET", "POST"])
def create_profile():
    return render_template("sign-up.html")

    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username is already taken")
            return redirect(url_for('signup'))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into session
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile"))

    return render_template("sign-up.html")


@app.route('/create-profile')
def create_new_profile():
    return render_template("create-profile.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if a user exists
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check hashed password
            if check_password_hash(
                 existing_user['password'], request.form.get('password')):
                    session['user'] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(
                        url_for("profile", username=session["user"]))
            else:
                # if password doesn't match
                flash("Incorrect Username and/or Password, Please try again")
                return redirect(url_for("home") + '#logInModal')
        else:
            # username does not exist
            flash("Incorrect Username and/or Password, Please try again")
            return redirect(url_for("home") + '#logInModal')

    return render_template("index.html" + '#logInModal')

    
@app.route("/logout")
def logout():
    flash("You have been logged out.")
    session.pop("user")
    return redirect(url_for("home"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
