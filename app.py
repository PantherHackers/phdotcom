import os

from flask import render_template, Flask, request, send_from_directory
from flask_scss import Scss

from app_helper import *

app = Flask(__name__)
Scss(app, asset_dir='assets/scss', static_dir='static/css')


@app.route('/index')
@app.route('/')
def index():
	return render_template('home.html', 
		nav_menu_items=nav_menu_items, 
		social_media_items=social_media_items)

@app.route('/blog')
def blog():
	return 'blog' 

@app.route('/events')
def events():
	return 'events'

@app.route('/about')
def about():
	return 'about'

@app.after_request
def add_header(r):
	r.headers['Pragma'] = 'no-cache'
	r.headers['Expires'] = '0'
	r.headers['Cache-Control'] = 'public, max-age=0'
	return r

if __name__ == '__main__':
	app.run(debug=True)