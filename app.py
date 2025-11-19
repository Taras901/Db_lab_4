import yaml
import urllib.parse
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("ПОМИЛКА: Файл 'config/config.yaml' не знайдено.")
    exit(1)

db_config = config.get('database', {})
db_user = db_config.get('user')
raw_pass = db_config.get('password')
db_host = db_config.get('host')
db_name = db_config.get('database_name')

encoded_pass = urllib.parse.quote_plus(str(raw_pass))
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{encoded_pass}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = automap_base()

with app.app_context():
    Base.prepare(autoload_with=db.engine)

Clients = Base.classes.clients
Trainers = Base.classes.trainers
Equipment = Base.classes.equipment
Services = Base.classes.services
Exercises = Base.classes.exercises
GymSchedule = Base.classes.gym_schedule
ClientVisits = Base.classes.client_visits

def row_to_dict(row):
    data = {}
    for column in row.__table__.columns:
        value = getattr(row, column.name)
        if isinstance(value, (datetime.date, datetime.datetime, datetime.time)):
            value = str(value)
        data[column.name] = value
    return data

@app.route('/')
def index():
    return jsonify({
        "status": "Online",
        "available_routes": [
            "/clients",
            "/trainers",
            "/equipment",
            "/services",
            "/exercises",
            "/schedule",
            "/visits"
        ]
    })

@app.route('/clients')
def get_clients():
    items = db.session.query(Clients).all()
    return jsonify([row_to_dict(item) for item in items])

@app.route('/trainers')
def get_trainers():
    items = db.session.query(Trainers).all()
    return jsonify([row_to_dict(item) for item in items])

@app.route('/equipment')
def get_equipment():
    items = db.session.query(Equipment).all()
    return jsonify([row_to_dict(item) for item in items])

@app.route('/services')
def get_services():
    items = db.session.query(Services).all()
    return jsonify([row_to_dict(item) for item in items])

@app.route('/exercises')
def get_exercises():
    items = db.session.query(Exercises).all()
    return jsonify([row_to_dict(item) for item in items])

@app.route('/schedule')
def get_schedule():
    items = db.session.query(GymSchedule).all()
    return jsonify([row_to_dict(item) for item in items])

@app.route('/visits')
def get_visits():
    items = db.session.query(ClientVisits).all()
    return jsonify([row_to_dict(item) for item in items])

if __name__ == '__main__':
    app.run(debug=True)