import os
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/companies')
def companies():
    return render_template("companies.html")


@app.route('/createProfile', methods=["GET", "POST"])
def create_profile():
    return render_template("createProfile.html")


if __name__ == "__main__":
    app.run(debug=True)
