"""
This script runs the FlaskWebProject1 application using a development server.
"""

from os import environ
from FlaskWebProject1 import app
from datetime import datetime
from flask import render_template, request, send_file
from FlaskWebProject1.PartD import *;

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/', methods=['POST'])
def home_post():
    text = request.form['u']
    processed_text = text.lower()
    results = myD.getHitList(processed_text)
    return render_template(
        'r.html',
        title='Results',
        year=datetime.now().year,
        message='Results for query ' + processed_text,
        data=results
    )


@app.route('/results/<path:filename>')
def results(filename):
    return send_file(filename)


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year
    )

myD = SearchEngine()
myD.crawlIndex()

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
