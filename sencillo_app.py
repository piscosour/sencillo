import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sencillo_classes import User, Payment

# config
DATABASE = '/tmp/sencillo.db'
DEBUG = True
SECRET_KEY = 'development'
USERNAME = 'admin'
PASSWORD = 'default'

# initialise the app
app = Flask(__name__)
app.config.from_object(__name__)

users = []

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# views

@app.route('/')
def index():
	if 'user' in session:
		return render_template('main.html', user=session['user'])
	else:
		return render_template('main.html')

@app.route('/registro', methods=['GET', 'POST'])
def new_user():
	if request.method == 'GET':
		return render_template('new-user.html')
	elif request.method == 'POST':
		new_user = User(request.form['username'], request.form['password'], request.form['email'], request.form['mobile'])
		users.append(new_user)
		session['user'] = new_user
		return redirect(url_for('user_profile', username=session['user'].username))

@app.route('/login', methods=['GET', 'POST'])
def login_user():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		for user in users:
			if user.username == request.form['username'] and user.password == request.form['password']:
				session['user'] = user
				return redirect(url_for('user_profile', username=session['user'].username))
		else:
			return False

@app.route('/<username>')
def user_profile(username):
	for user in users:
		if username == user.username:
			return render_template('profile.html', user=user)
	else:
		return False

# run app

if __name__ == "__main__":
	app.secret_key = 'T:\xb9\xc1\xf9\xf2@\x89\xa8\xe2K\xf6\x1a\x92\xd3\x92\xce\x88\x98{bO\xcf<'
	app.run()

