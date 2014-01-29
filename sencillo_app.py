#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from sencillo_classes import User, Payment
from codes import codes

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

# views

@app.route('/')
def index():
	if 'user' in session:
		return render_template('main.html', user=fetch_user_data(session['user']))
	else:
		return render_template('main.html')

@app.route('/registro', methods=['GET', 'POST'])
def new_user():
	if request.method == 'GET':
		return render_template('new-user.html')
	elif request.method == 'POST':
		if check_user(request.form['username']) is False:
			new_user = User(request.form['username'], request.form['password'], request.form['email'], request.form['mobile'])
			users.append(new_user)
			g.db.execute('insert into users (username, password, email, mobile, credit) values (?, ?, ?, ?, ?)', 
						 [request.form['username'], request.form['password'], request.form['email'], request.form['mobile'], 0])
			g.db.commit()
			flash('Tu cuenta ha sido creada con éxito')
			session['user'] = new_user.username
			session['logged_in'] = True
			return redirect(url_for('user_profile', username=session['user']))
		else:
			flash('El nombre de usuario ya está registrado.')
			return redirect(url_for('new_user'))

@app.route('/login', methods=['GET', 'POST'])
def login_user():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		cur = g.db.execute('select username, password from users order by id asc')
		for row in cur.fetchall():
			if request.form['username'] == row[0] and request.form['password'] == row[1]:
				session['user'] = row[0]
				session['logged_in'] = True
				return redirect(url_for('user_profile', username=session['user']))
		else:
			return False

@app.route('/logout')
def logout_user():
	session.pop('user', None)
	return redirect(url_for('index'))

@app.route('/<username>')
def user_profile(username):
	if username == session['user']:
			history = gen_history(username)
			return render_template('profile.html', user=fetch_user_data(session['user']), history=history)
	else:
		for entry in users:
			if username == entry.username:
				return render_template('public-profile.html', username=username)
		else:
			return False

@app.route('/envio', methods=['GET', 'POST'])
def new_payment():
	if request.method == 'GET':
		return render_template('payment.html', user=fetch_user_data(session['user']))
	elif request.method == 'POST':
		sender = fetch_user_data(session['user'])
		if sender.credit > request.form['amount']:
			g.db.execute('insert into payments (sender, recipient, amount, timestamp, description) values (?, ?, ?, ?, ?)',
						 [session['user'], request.form['recipient'], request.form['amount'], str(datetime.datetime.now()).split('.')[0], request.form['description']])
			g.db.commit()
			sender.credit = sender.credit - request.form['amount']
			recipient = fetch_user_data(request.form['recipient'])
			recipient.credit = recipient.credit + request.form['amount']
			update_user_data(sender)
			update_user_data(recipient)
			flash('Tu transacción ha sido realizada')
			return redirect(url_for('user_profile', username=session['user']))

@app.route('/recarga', methods=['GET', 'POST'])
def new_credit():
	if request.method == 'GET':
		return render_template('credit.html', user=fetch_user_data(session['user']))
	elif request.method == 'POST':
		if request.form['code'] in codes:
			sender = fetch_user_data(session['user'])
			g.db.execute('insert into payments (sender, recipient, amount, timestamp, description) values (?, ?, ?, ?, ?)',
						 [session['user'], session['user'], 10, str(datetime.datetime.now()).split('.')[0], 'Nueva recarga'])
			g.db.commit()
			sender.credit = sender.credit + 10
			update_user_data(sender)
			flash('Tu recarga ha sido realizada')
			return redirect(url_for('user_profile', username=session['user']))

# admin views

@app.route('/users')
def user_list(users=users):
	cur = g.db.execute('select id, username, email, mobile, credit from users order by id asc')
	users = [dict(id=row[0], username=row[1], email=row[2], phone=row[3], credit=row[4]) for row in cur.fetchall()]
	return render_template('user-list.html', user_data=users)

# helper functions
def check_user(username):
	cur = g.db.execute('select username from users order by id asc')
	for row in cur.fetchall():
		if username == row[0]:
			return True
	else:
		return False

def fetch_user_data(username):
	if check_user(username) is True:
		cur = g.db.execute('select username, email, mobile, credit from users where username = ?', [username])
		result = cur.fetchall()
		data = result[0]
		user = User(data[0], data[1], data[3], data[2])
		return user
	else:
		return False

def update_user_data(user):
	g.db.execute('update users set username = ?, email = ?, mobile = ?, credit = ? where username = ?',
				 [user.username, user.email, user.mobile, user.credit, user.username])
	g.db.commit()


def gen_history(username):
	cur = g.db.execute('select sender, recipient, amount, timestamp, description from payments where sender = ? or recipient = ?', [username, username])
	payments = [dict(sender=row[0], recipient=row[1], amount=row[2], timestamp=row[3], description=row[4]) for row in cur.fetchall()]
	if len(payments) > 0:
		return payments
	else:
		return None

# database functions

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

# run app

if __name__ == "__main__":
	app.secret_key = 'T:\xb9\xc1\xf9\xf2@\x89\xa8\xe2K\xf6\x1a\x92\xd3\x92\xce\x88\x98{bO\xcf<'
	app.run()

