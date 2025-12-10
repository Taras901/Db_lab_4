from flask import Blueprint, request, jsonify
from my_project.service.client_service import ClientService

client_bp = Blueprint('client_bp', __name__)
service = ClientService()

# 1. Отримати всіх
@client_bp.route('/clients', methods=['GET'])
def get_clients():
    return jsonify(service.get_all()), 200

# 2. Створити клієнта (Процедура)
@client_bp.route('/clients', methods=['POST'])
def add_client():
    success, message = service.create_client(request.json)
    if success: return jsonify({"message": message}), 201
    return jsonify({"message": message}), 400

# 3. Генерація 10 ботів (Процедура While)
@client_bp.route('/clients/generate', methods=['POST'])
def generate_dummy():
    service.generate_dummies()
    return jsonify({"message": "10 Dummy clients added"}), 201

# 4. Зв'язок M:M (Процедура)
@client_bp.route('/programs/link', methods=['POST'])
def link_exercise():
    success, message = service.link_exercise(request.json)
    if success: return jsonify({"message": message}), 200
    return jsonify({"message": message}), 400

# 5. Статистика Max/Min/Sum (Функції)
@client_bp.route('/services/stats', methods=['GET'])
def get_stats():
    return jsonify(service.get_service_stats()), 200

# 6. Курсор (Створення таблиць)
@client_bp.route('/clients/split', methods=['POST'])
def split_cursor():
    return jsonify({"result": service.split_tables()}), 200

# --- МАРШРУТИ ДЛЯ ТРИГЕРІВ ---

# 7. Шафка (Тригер 1)
@client_bp.route('/lockers', methods=['POST'])
def add_locker():
    success, message = service.add_locker(request.json)
    status = 201 if success else 400
    return jsonify({"message": message}), status

# 8. Тренер (Тригер 3a - Телефон)
@client_bp.route('/trainers', methods=['POST'])
def add_trainer():
    success, message = service.add_trainer(request.json)
    status = 201 if success else 400
    return jsonify({"message": message}), status

# 9. Ціна (Тригер 3b - Заборона Update)
@client_bp.route('/services/price', methods=['PUT'])
def update_price():
    success, message = service.change_price(request.json)
    status = 200 if success else 400
    return jsonify({"message": message}), status

# 10. Програма (Тригер 3c - Заборона Delete)
@client_bp.route('/programs', methods=['DELETE'])
def delete_program():
    success, message = service.remove_program(request.json)
    status = 200 if success else 400
    return jsonify({"message": message}), status