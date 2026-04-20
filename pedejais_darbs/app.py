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

@app.route('/deklinesana', methods=['POST', 'GET'])
def deklinet():
	if request.method == 'POST':
		vards = request.form.get('vards')
		dzimums = request.form.get('dzimte')

		if not vards:
			return render_template('deklinesana.html')

		if vards.endswith('s') and dzimums == 'Siev. dz.':
			deklinacija = 6
		elif vards.endswith('s') or vards.endswith('š'):
			deklinacija = 1
		elif vards.endswith('is'):
			deklinacija = 2
		elif vards.endswith('us'):
			deklinacija = 3
		elif vards.endswith('a'):
			deklinacija = 4
		elif vards.endswith('e'):
			deklinacija = 5
		else:
			deklinacija = 0
		return render_template('deklinesana.html', deklinacija=deklinacija)

		conn = sqlite3.connect("vardi.db")
		cur = conn.cursor()
		cur.execute(
			"INSERT INTO gramatas (Vards, Dzimums, Deklinacija) VALUES (?, ?, ?)",
			(vards.capitalize, dzimums, deklinacija)
		)
		conn.commit()
		conn.close()
	return render_template('deklinesana.html')

@app.route('/info')
def info():
	return render_template('info.html')

if __name__ == '__main__':
	app.run(debug=True)