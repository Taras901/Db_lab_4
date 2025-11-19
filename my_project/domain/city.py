from app import db

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    people = db.relationship('Person', back_populates='city', lazy='dynamic')

    def to_dto(self):
        return {
            'id': self.id,
            'name': self.name
        }