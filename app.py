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
    companies = list(mongo.db.companies.find())
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
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "companyName": request.form.get("companyName"),
            "companyAddress": request.form.get("companyAddress"),
            "companyWebsite": request.form.get("companyWebsite")
        }
        mongo.db.Users.insert_one(register)
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("sign-up.html")


@app.route('/createProfile', methods=["GET", "POST"])
def create_profile():
    """
        create company profile when user is logged in.
    """
    username = mongo.db.Users.find_one(
        {'username': session['user']})['username']
    if request.method == 'POST':
        profile = {
            'approach_entrance': {
                'parking': request.form.get('parking'),
                'entrances': request.form.get('entrances')
            },
            'facilities': {
                'toilets': request.form.get('toilets'),
                'office': request.form.get('office'),
                'social_area': request.form.get('socialArea'),
                'special_equipments': request.form.get('specialEquipments'),
                'others': request.form.get('facilitiesOthers')
            },
            'assistive_tech': {
                'available_tech': request.form.get('assist'),
                'others': request.form.get('technologyOthers')
            },
            'working_flexibility': request.form.get('workingFlexibility'),
            'hr_policies': {
                'hr_policies1':  request.form.get('hrPolicies1'),
                'hr_policies2':  request.form.get('hrPolicies2'),
            },
            'inclusive_culture': {
                'inclusive_culture1':  request.form.get('companyCulture1'),
                'inclusive_culture2':  request.form.get('companyCulture2'),
                'inclusive_culture3':  request.form.get('companyCulture1'),
            },
            'media': {
                'companyLogo':  request.form.get('companyLogo'),
                'company_banner_img': {
                    'url': request.form.get('companyBannerImg'),
                    'desc': request.form.get('companyBannerDesc'),
                },
                'image1': {
                    'url': request.form.get('companyImg1'),
                    'desc': request.form.get('companyImg1Desc')
                },
                'image2': {
                    'url': request.form.get('companyImg2'),
                    'desc': request.form.get('companyImg2Desc')
                },
                'image3': {
                    'url': request.form.get('companyImg3'),
                    'desc': request.form.get('companyImg3Desc')
                },
                'image4': {
                    'url': request.form.get('companyImg4'),
                    'desc': request.form.get('companyImg4Desc')
                },
                'image5': {
                    'url': request.form.get('companyImg5'),
                    'desc': request.form.get('companyImg5Desc')
                },
            }
        }
        mongo.db.companies.insert_one(profile)
        flash('Profule successfully created')
        return redirect(url_for('profile'))
    return render_template("create-profile.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check if a user exists
        existing_user = mongo.db.Users.find_one(
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
    username = mongo.db.Users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route('/companies/<company_name>')
def company_profile(company_name):
    company = mongo.db.companies.find_one(
        {'companyName': company_name}
    )
    return render_template('profile.html', company=company)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
