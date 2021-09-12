import os
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/companies')
def companies():
    return render_template("companies.html")

if __name__ == "__main__":
    app.run(debug=True)