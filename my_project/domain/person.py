from app import db

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    
    city = db.relationship('City', back_populates='people')

    def to_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'city_id': self.city_id,
            'city_name': self.city.name if self.city else None 
        }