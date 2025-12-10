from my_project.db import get_connection
import mysql.connector

class ClientDAO:
    def get_all_clients(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clients")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def create_client_procedure(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('sp_create_client', (data['first_name'], data['last_name'], data['email'], data['phone']))
            conn.commit()
            return True, "Client created"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    def insert_dummy_clients(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('sp_insert_dummy_clients')
            conn.commit()
            return True, "Dummy clients added"
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    def link_program_exercise(self, p_name, ex_name, sets, reps):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('sp_link_program_exercise_by_name', (p_name, ex_name, sets, reps))
            conn.commit()
            return True, "Exercise linked successfully"
        except Exception as e:
            return False, str(e) # Поверне помилку, якщо такий зв'язок вже є
        finally:
            cursor.close()
            conn.close()

    def get_price_stats(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('sp_get_price_stats')
            for res in cursor.stored_results():
                return res.fetchone()
        except Exception as e:
            return None
        finally:
            cursor.close()
            conn.close()

    def run_cursor_split(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.callproc('sp_cursor_split_clients')
            # Отримуємо повідомлення про успіх (SELECT 'Success...')
            for res in cursor.stored_results():
                return res.fetchall()
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
            conn.close()

    # --- МЕТОДИ ДЛЯ ТРИГЕРІВ (ЗАВДАННЯ 1 та 3) ---

    # 1. Шафки (Завдання 1)
    def assign_locker(self, client_id, locker_num):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Client_Lockers (client_id, locker_number, assigned_date) VALUES (%s, %s, CURDATE())", (client_id, locker_num))
            conn.commit()
            return True, "Locker assigned"
        except Exception as e:
            return False, str(e) # Тут спрацює тригер "Client ID does not exist"
        finally:
            cursor.close()
            conn.close()

    # 2. Тренер (Завдання 3.a - телефон)
    def create_trainer(self, name, phone):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Trainers (first_name, last_name, phone) VALUES (%s, 'Test', %s)", (name, phone))
            conn.commit()
            return True, "Trainer created"
        except Exception as e:
            return False, str(e) # Тут спрацює тригер "...end with 00"
        finally:
            cursor.close()
            conn.close()

    # 3. Ціна (Завдання 3.b - update)
    def update_service_price(self, service_id, new_price):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Services SET price = %s WHERE service_id = %s", (new_price, service_id))
            conn.commit()
            return True, "Price updated"
        except Exception as e:
            return False, str(e) # Тут спрацює тригер "forbidden"
        finally:
            cursor.close()
            conn.close()

    # 4. Програма (Завдання 3.c - delete)
    def delete_program(self, prog_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM General_Programs WHERE program_id = %s", (prog_id,))
            conn.commit()
            return True, "Program deleted"
        except Exception as e:
            return False, str(e) # Тут спрацює тригер "forbidden"
        finally:
            cursor.close()
            conn.close()