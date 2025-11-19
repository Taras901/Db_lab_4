from app import app
from flask import request, jsonify
from ..service import city_service

@app.route('/cities', methods=['GET'])
def get_cities():
    cities_dto = city_service.get_all_cities()
    return jsonify(cities_dto), 200

@app.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    city_dto = city_service.get_city_by_id(city_id)
    if not city_dto:
        return jsonify({"error": "Місто не знайдено"}), 404
    return jsonify(city_dto), 200

@app.route('/cities', methods=['POST'])
def create_city():
    data = request.json
    city_dto, error = city_service.create_city(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(city_dto), 201

@app.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.json
    city_dto, error = city_service.update_city(city_id, data)
    if error:
        return jsonify({"error": error}), (404 if "не знайдено" in error else 400)
    return jsonify(city_dto), 200

@app.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    success = city_service.delete_city(city_id)
    if not success:
        return jsonify({"error": "Місто не знайдено"}), 404
    return jsonify({"message": "Місто видалено"}), 200

@app.route('/cities/<int:city_id>/people', methods=['GET'])
def get_people_for_city(city_id):
    people_dto_list = city_service.get_people_in_city(city_id)
    
    if people_dto_list is None:
        return jsonify({"error": "Місто не знайдено"}), 404
        
    return jsonify(people_dto_list), 200