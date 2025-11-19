from ..dao import city_dao

def get_all_cities():
    cities = city_dao.get_all_cities()
    return [city.to_dto() for city in cities]

def get_city_by_id(city_id):
    city = city_dao.get_city_by_id(city_id)
    if city:
        return city.to_dto()
    return None

def create_city(data):
    name = data.get('name')
    if not name:
        return None, "Ім'я міста є обов'язковим"
        
    city = city_dao.create_city(name)
    return city.to_dto(), None

def update_city(city_id, data):
    name = data.get('name')
    if not name:
        return None, "Ім'я міста є обов'язковим"
        
    city = city_dao.update_city(city_id, name)
    if not city:
        return None, "Місто не знайдено"
        
    return city.to_dto(), None

def delete_city(city_id):
    city = city_dao.delete_city(city_id)
    if not city:
        return False
    return True

def get_people_in_city(city_id):
    people_models = city_dao.get_people_in_city(city_id)
    if people_models is None:
        return None
    return [person.to_dto() for person in people_models]