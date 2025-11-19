import yaml
import urllib.parse
import datetime
from flask import Flask, jsonify, request
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
ClientVisits = Base.classes.client_visits
Exercises = Base.classes.exercises
ProgramExercises = Base.classes.program_exercises

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
    return jsonify({"status": "Online", "message": "API готове!"})

@app.route('/clients', methods=['GET'])
def get_clients():
    items = db.session.query(Clients).all()
    return jsonify([row_to_dict(item) for item in items])

@app.route('/clients', methods=['POST'])
def add_client():
    data = request.json
    try:
        new_client = Clients(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email'),
            phone=data.get('phone'),
            registration_date=data.get('registration_date', datetime.date.today())
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({"message": "Створено", "client": row_to_dict(new_client)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.json
    client = db.session.query(Clients).get(client_id)
    if not client: return jsonify({"error": "Not found"}), 404
    
    try:
        if 'first_name' in data: client.first_name = data['first_name']
        if 'last_name' in data: client.last_name = data['last_name']
        if 'email' in data: client.email = data['email']
        if 'phone' in data: client.phone = data['phone']
        db.session.commit()
        return jsonify({"message": "Оновлено", "client": row_to_dict(client)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = db.session.query(Clients).get(client_id)
    if not client: return jsonify({"error": "Not found"}), 404
    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Видалено"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/clients/<int:client_id>/visits', methods=['GET'])
def get_client_visits(client_id):
    visits = db.session.query(ClientVisits).filter_by(client_id=client_id).all()
    return jsonify([row_to_dict(v) for v in visits])

@app.route('/programs/<int:program_id>/exercises', methods=['GET'])
def get_program_exercises(program_id):
    results = db.session.query(Exercises).join(
        ProgramExercises, Exercises.exercise_id == ProgramExercises.exercise_id
    ).filter(ProgramExercises.program_id == program_id).all()
    return jsonify([row_to_dict(ex) for ex in results])

if __name__ == '__main__':
    app.run(debug=True)