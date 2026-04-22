from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'slepena_atslega'

@app.route('/')
def sakums():
	return render_template('sakums.html')

@app.context_processor
def teicieni():
    teksts = ['Deklinēšana latviešu valodā ir lietvārdu, īpašības vārdu, vietniekvārdu un skaitļa vārdu locīšana pa locījumiem, piemēram, nominatīvu, ģenitīvu, datīvu, akuzatīvu, instrumentāli un lokatīvu.', 'Katrs locījums atbild uz noteiktu jautājumu un palīdz saprast vārda funkciju teikumā.', 'Piemēram, vārds “skola” var kļūt par “skolas”, “skolai”, “skolu” un tā tālāk, atkarībā no konteksta.', 'Šī sistēma ļauj valodai būt elastīgai un precīzai, kas ir īpaši svarīgi sarežģītākos teikumos un tekstos.']
    rindina = random.choice(teksts)
    return dict(rindina=rindina)

@app.route('/locijumi')
def locijumi():
	return render_template('locijumi.html')

@app.route('/deklinesana', methods=['POST', 'GET'])
def deklinet():
	conn = sqlite3.connect("vardi.db")
	cur = conn.cursor()

	if request.method == 'POST':
		vards = request.form.get('vards').capitalize()
		dzimums = request.form.get('dzimte')

		if not vards or not dzimums:
			conn.close()
			return render_template('deklinesana.html')

		if vards.endswith('s') and dzimums == 'Siev. dz.':
			deklinacija = 6
		elif vards.endswith('is'):
			deklinacija = 2
			dzimums = 'Vīr. dz.'
		elif vards.endswith('us'):
			deklinacija = 3
			dzimums = 'Vīr. dz.'
		elif vards.endswith('š') or vards.endswith('s'):
			deklinacija = 1
			dzimums = 'Vīr. dz.'
		elif vards.endswith('a'):
			deklinacija = 4
			dzimums = 'Siev. dz.'
		elif vards.endswith('e'):
			deklinacija = 5
			dzimums = 'Siev. dz.'
		else:
			deklinacija = 0

		cur.execute(
			"SELECT * FROM Vardi WHERE Vards = ? AND Dzimums = ?",
			(vards, dzimums)
			)
		existing = cur.fetchone()

		if existing:
			conn.close()
		else:
			cur.execute(
				"INSERT INTO Vardi (Vards, Dzimums, Deklinacija) VALUES (?, ?, ?)",
				(vards, dzimums, deklinacija)
				)
			conn.commit()
			conn.close()

		return redirect(url_for('results', deklinacija=deklinacija, vards=vards))

	return render_template('deklinesana.html')


@app.route('/results')
def results():
	locijumi = []
	if deklinacija==1:
		
	return render_template('results.html')


@app.route('/info')
def info():
	return render_template('info.html')

if __name__ == '__main__':
	app.run(debug=True)