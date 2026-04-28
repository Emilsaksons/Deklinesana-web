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

		if vards in ['Mēness', 'Akmens', 'Asmens', 'Rudens', 'Ūdens', 'Zibens', 'Suns', 'Sāls']:
			deklinacija = '2*'
		elif vards.endswith('s') and dzimums == 'Siev. dz.':
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


@app.route('/results', methods=['GET', 'POST'])
def results():
	deklinacija=request.args.get('deklinacija')
	vards=request.args.get('vards')
	locijumi = []
	if deklinacija == '1':
		sakne = vards[:-1]
		nominativs = vards
		genetivs = sakne + 'a'
		dativs = sakne + 'am'
		akuzativs = sakne + 'u'
		instrumentalis = 'ar ' + sakne + 'u'
		lokativs = sakne + 'ā'
		vokatīvs = sakne + '!'
		locijumi.extend([nominativs,genetivs,dativs,akuzativs,instrumentalis,lokativs,vokatīvs])

	elif deklinacija == '2':
		sakne = vards[:-2]
		nominativs = vards
		if vards.endswith(('bis', 'mis', 'pis', 'vis')):
			genetivs = sakne + 'ja'
		elif vards.endswith(('tis', 'sis')):
			sakne = vards[:-3]
			genetivs = sakne + 'ša'
		elif vards.endswith(('dis', 'zis')):
			sakne = vards[:-3]
			genetivs = sakne + 'ža'
		elif vards.endswith('cis'):
			sakne = vards[:-3]
			genetivs = sakne + 'ča'
		elif vards.endswith('nis'):
			sakne = vards[:-3]
			genetivs = sakne + 'ņa'
		elif vards.endswith('lis'):
			sakne = vards[:-3]
			genetivs = sakne + 'ļa'
		elif vards.endswith('snis'):
			sakne = vards[:-4]
			genetivs = sakne + 'šņa'
		elif vards.endswith('znis'):
			sakne = vards[:-4]
			genetivs = sakne + 'žņa'
		elif vards.endswith('slis'):
			sakne = vards[:-4]
			genetivs = sakne + 'šļa'
		elif vards.endswith('zlis'):
			sakne = vards[:-4]
			genetivs = sakne + 'žļa'
		elif vards.endswith('lnis'):
			sakne = vards[:-3]
			genetivs = sakne + 'ļņa'
		dativs = sakne + 'im'
		akuzativs = sakne + 'i'
		instrumentalis = 'ar ' + sakne + 'i'
		lokativs = sakne + 'ī'
		vokatīvs = vards[:-1] + '!'
		locijumi.extend([nominativs,genetivs,dativs,akuzativs,instrumentalis,lokativs,vokatīvs])


	elif deklinacija == '2*':
		sakne = vards[:-1]
		nominativs = vards
		genetivs = vards
		dativs = sakne + 'im'
		akuzativs = sakne + 'i'
		instrumentalis = 'ar ' + sakne + 'i'
		lokativs = sakne + 'ī'
		vokatīvs = vards + 'i' + '!'
		locijumi.extend([nominativs,genetivs,dativs,akuzativs,instrumentalis,lokativs,vokatīvs])

	elif deklinacija == '3':
		sakne = vards[:-2]
		nominativs = vards
		genetivs = vards
		dativs = sakne + 'um'
		akuzativs = sakne + 'u'
		instrumentalis = 'ar ' + sakne + 'u'
		lokativs = sakne + 'ū'
		vokatīvs = vards + '!'
		locijumi.extend([nominativs,genetivs,dativs,akuzativs,instrumentalis,lokativs,vokatīvs])

	elif deklinacija == '4':
		sakne = vards[:-1]
		nominativs = vards
		genetivs = sakne + 'as'
		dativs = sakne + 'ai'
		akuzativs = sakne + 'u'
		instrumentalis = 'ar ' + sakne + 'u'
		lokativs = sakne + 'ā'
		vokatīvs = vards + '!'
		locijumi.extend([nominativs,genetivs,dativs,akuzativs,instrumentalis,lokativs,vokatīvs])

	elif deklinacija == '5':
		sakne = vards[:-1]
		nominativs = vards
		genetivs = sakne + 'es'
		dativs = sakne + 'ei'
		akuzativs = sakne + 'i'
		instrumentalis = 'ar ' + sakne + 'i'
		lokativs = sakne + 'ē'
		vokatīvs = vards + '!'
		locijumi.extend([nominativs,genetivs,dativs,akuzativs,instrumentalis,lokativs,vokatīvs])

	elif deklinacija == '6':
		sakne = vards[:-1]
		nominativs = vards
		genetivs = vards
		dativs = sakne + 'ij'
		akuzativs = sakne + 'i'
		instrumentalis = 'ar ' + sakne + 'i'
		lokativs = sakne + 'ī'
		vokatīvs = vards + '!'
		locijumi.extend([nominativs,genetivs,dativs,akuzativs,instrumentalis,lokativs,vokatīvs])
		
	return render_template('results.html', locijumi=locijumi)


@app.route('/info')
def info():
	return render_template('info.html')

if __name__ == '__main__':
	app.run(debug=True)