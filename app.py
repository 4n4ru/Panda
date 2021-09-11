import os
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/createProfile')
def create_profile():
    return render_template("createProfile.html")

if __name__ == "__main__":
    app.run(debug=True)



