
from flask import render_template

from . import app

@app.route('/index.jsp')
@app.route('/index/')
def home():
    return render_template('index.html', author='Mary')

@app.route('/contact_us.jsp')
@app.route('/contact_us/')
def contact_us():
    return render_template('contact_us.html');