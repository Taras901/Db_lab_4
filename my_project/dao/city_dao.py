from app import db
from ..domain.city import City
from ..domain.person import Person

def get_all_cities():
    return City.query.all()

def get_city_by_id(city_id):
    return City.query.get(city_id)

def create_city(name):
    new_city = City(name=name)
    db.session.add(new_city)
    db.session.commit()
    return new_city

def update_city(city_id, name):
    city = get_city_by_id(city_id)
    if city:
        city.name = name
        db.session.commit()
    return city

def delete_city(city_id):
    city = get_city_by_id(city_id)
    if city:
        db.session.delete(city)
        db.session.commit()
    return city

def get_people_in_city(city_id):
    city = get_city_by_id(city_id)
    if city:
        return city.people.all() 
    return None