# -*- coding: utf-8 -*-

from flask import Flask, render_template

from teseo_model import Thesis, Person, Descriptor, Department
from teseo_model import University, Advisor, PanelMember
from teseo_model import Base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, extract, func

import json

USER = 'teseo'
PASS = 'teseo'
DB_NAME = 'teseo'

engine = create_engine('mysql://%s:%s@localhost/%s?charset=utf8' % (USER, PASS, DB_NAME))

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route("/university/<university_id>/progression")
def show_progression(university_id):
	
	university = session.query(University).filter_by(id=university_id).first()
	values = session.query(Thesis.defense_date, func.count(Thesis.id)).filter_by(university=university).group_by(extract('year', Thesis.defense_date))

	data = {}
	data['key'] = university.name

	rows = []
	for v in values:
		row = {}
		row['label'] = v[0].year
		row['value'] = v[1]
		rows.append(row)

	data['values'] = rows  

	return render_template('progression.html', university=university, data=json.dumps(data))

if __name__ == "__main__":
    app.run(debug=True)