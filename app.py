import os
from flask import Flask, jsonify

app = Flask(__name__)

movies = [
     {
         "name": "The Shawshank Redemption",
         "casts": ["Tim Robbins", "Morgan Freeman", "Bob Gunton"],
         "genres": ["Drama"]
     },
     {
        "name": "The Godfather ",
        "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
        "genres": ["Crime", "Drama"]
     }
 ]


@app.route('/')
@app.route('/movies')
def hello():
    return {'hello': 'world'}
    return jsonify(movies)


app.run()