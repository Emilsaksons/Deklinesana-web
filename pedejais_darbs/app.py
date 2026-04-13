from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'slepena_atslega'

@app.route('/')
def sakums():
	return render_template('sakums.html')

@app.route('/locijumi')
def locijumi():
	return render_template('locijumi.html')

@app.route('/deklinesana')
def deklinet():
	return render_template('deklinesana.html')

@app.route('/info')
def info():
	return render_template('info.html')

if __name__ == '__main__':
	app.run(debug=True)