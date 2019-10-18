from flask import render_template, request

from dash_package.dashboard import app

from dash_package.functions import *

@app.server.route('/dash')
def dashboard():
    return app.index()

@app.server.route('/hello')
def hello():
    return render_template('home.html')