from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from app.hive_ic import IntraAPIClient
from datetime import datetime
from . import main

db = SQLAlchemy()
ic = IntraAPIClient()
CAMPUS_ID = '13'
REDIRECT_URI = 'http://localhost:5000/login'

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    return render_template('index.html', client_id=ic.client_id, redirect_uri=REDIRECT_URI)

@main.route('/login')
def get_token():
	api_code = request.args.get('code', type = str)
	response = requests.post(ic.token_url, params={'grant_type':'authorization_code', 'client_id': ic.client_id, 'client_secret': ic.client_secret, 'code': api_code, 'redirect_uri': REDIRECT_URI})
	token = json.loads(response.content)['access_token']
	response = requests.get(ic.api_url+'me', params={'access_token':token})
	"""TODO: Authenticate user. Also check campus:
	if (json.loads(response.content)['staff?'] == True):
		return render_template('menu.html')
	else:
		return render_template('not_staff.html')
	"""
	return render_template('menu.html')

@main.route('/assign_seats')
def assign_seats():
	#TODO: Autheticate user
    return render_template('assign_seats.html')

def get_exam_by_date(date: str):
	exams = ic.pages_threaded('campus/'+CAMPUS_ID+'/exams')
	if date == '0':
		date = datetime.now().strftime("%Y-%m-%d")
	for exam in exams:
		if exam['begin_at'][:10] == date:
			return jsonify(exam)
	return jsonify(id=-1)

import sys #db trials
def get_exam_by_id(id: int):
	if True: #db trials
		db.engine.execute("CREATE TABLE IF NOT EXISTS exams(id INTEGER NOT NULL PRIMARY KEY);")
		db.engine.execute("DELETE FROM exams WHERE 1=1;")
		db.engine.execute("INSERT INTO exams VALUES (2707);")
		dbr = db.engine.execute("SELECT * FROM exams;")
		for r in dbr:
			print(r, file=sys.stderr)
	

	exams = ic.pages_threaded('campus/'+CAMPUS_ID+'/exams')
	for exam in exams:
		if int(exam['id']) == id:
			return jsonify(exam)
	return jsonify(id=-1)

@main.route('/get_exam')
def get_exam():
	id = request.args.get('id', default=-1, type=int)
	if id != -1:
		return get_exam_by_id(int(id))
	else:
		date = request.args.get('date', default='0', type=str)
		return get_exam_by_date(date)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
