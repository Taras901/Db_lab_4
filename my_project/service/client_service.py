from my_project.dao.client_dao import ClientDAO

class ClientService:
    def __init__(self):
        self.dao = ClientDAO()

    def get_all(self):
        return self.dao.get_all_clients()

    def create_client(self, data):
        return self.dao.create_client_procedure(data)

    def generate_dummies(self):
        return self.dao.insert_dummy_clients()

    def link_exercise(self, data):
        return self.dao.link_program_exercise(data['program_name'], data['exercise_name'], data['sets'], data['reps'])

    def get_service_stats(self):
        return self.dao.get_price_stats()

    def split_tables(self):
        return self.dao.run_cursor_split()

    # --- Нові методи для тригерів ---
    
    def add_locker(self, data):
        return self.dao.assign_locker(data['client_id'], data['locker_number'])

    def add_trainer(self, data):
        return self.dao.create_trainer(data['name'], data['phone'])

    def change_price(self, data):
        return self.dao.update_service_price(data['id'], data['price'])

    def remove_program(self, data):
        return self.dao.delete_program(data['id'])