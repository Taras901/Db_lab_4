from app import db
from ..domain.models import (
    Client, Trainer, Equipment, WorkoutProgram, Service,
    ClientService, Exercise, TrainerSchedule, ClientProgram
)

# ---------------- Client Service ----------------
class ClientServiceManager:
    @staticmethod
    def get_all():
        return Client.query.all()

    @staticmethod
    def get_by_id(client_id):
        return Client.query.get(client_id)

    @staticmethod
    def create(data):
        client = Client(**data)
        db.session.add(client)
        db.session.commit()
        return client

    @staticmethod
    def update(client_id, data):
        client = Client.query.get(client_id)
        if not client:
            return None
        for key, value in data.items():
            if hasattr(client, key):
                setattr(client, key, value)
        db.session.commit()
        return client

    @staticmethod
    def delete(client_id):
        client = Client.query.get(client_id)
        if not client:
            return False
        db.session.delete(client)
        db.session.commit()
        return True

# ---------------- Trainer Service ----------------
class TrainerServiceManager:
    @staticmethod
    def get_all():
        return Trainer.query.all()

    @staticmethod
    def get_by_id(trainer_id):
        return Trainer.query.get(trainer_id)

    @staticmethod
    def create(data):
        trainer = Trainer(**data)
        db.session.add(trainer)
        db.session.commit()
        return trainer

    @staticmethod
    def delete(trainer_id):
        trainer = Trainer.query.get(trainer_id)
        if not trainer:
            return False
        db.session.delete(trainer)
        db.session.commit()
        return True

# ---------------- Equipment Service ----------------
class EquipmentServiceManager:
    @staticmethod
    def get_all():
        return Equipment.query.all()

    @staticmethod
    def create(data):
        eq = Equipment(**data)
        db.session.add(eq)
        db.session.commit()
        return eq

# ---------------- Workout Program Service ----------------
class WorkoutProgramServiceManager:
    @staticmethod
    def get_all():
        return WorkoutProgram.query.all()

    @staticmethod
    def create(data):
        prog = WorkoutProgram(**data)
        db.session.add(prog)
        db.session.commit()
        return prog

# ---------------- Service (Business) Manager ----------------
# Це для таблиці 'services' (абонементи)
class GymServiceManager:
    @staticmethod
    def get_all():
        return Service.query.all()

    @staticmethod
    def create(data):
        srv = Service(**data)
        db.session.add(srv)
        db.session.commit()
        return srv

# ---------------- Exercise Service ----------------
class ExerciseServiceManager:
    @staticmethod
    def get_all():
        return Exercise.query.all()