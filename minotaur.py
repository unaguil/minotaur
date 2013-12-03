from flask import Flask, render_template

from teseo_model import Thesis, Person, Descriptor, Department
from teseo_model import University, Advisor, PanelMember
from teseo_model import Base

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

USER = 'teseo'
PASS = 'teseo'
DB_NAME = 'teseo'

engine = create_engine('mysql://%s:%s@localhost/%s?charset=utf8' % (USER, PASS, DB_NAME))

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/university/<university_id>/progression")
def show_progression(university_id):
	university = session.query(University).filter_by(id=university_id).first()
	return render_template('progression.html', university_id=university_id, university_name=university.name)

if __name__ == "__main__":
    app.run(debug=True)