# models.py
import sqlite3
import logging

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('app.db')
        self.create_user_table()
        self.create_todo_table()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            CreatedOn DATE DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)

    def create_todo_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT,
            DueDate DATE,
            UserId INTEGER,
            FOREIGN KEY (UserId) REFERENCES User (id)
        );
        """
        self.conn.execute(query)

class UserModel:
    TABLENAME = "User"

    def __init__(self):
        # Initialize the connection to the database
        self.conn = sqlite3.connect('app.db')

    def __del__(self):
        # Ensure that the connection is closed
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        try:
            existing_user = self.get_by_username(params["Username"])
            if existing_user:
                return existing_user

            query = f'INSERT INTO {self.TABLENAME} (Username, Password) VALUES (?, ?)'
            self.conn.execute(query, (params["Username"], params["Password"]))  
            self.conn.commit()  # Commit the transaction
            
            # Fetch and return the newly created user
            return self.get_by_username(params["Username"])
        except Exception as e:
            print("An error occurred while creating the user: %s", e)  # Use logger to log the error
            return None


    def get_by_username(self, username):
        try:
            query = f'SELECT * FROM {self.TABLENAME} WHERE Username = ?'
            cursor = self.conn.execute(query, (username,))
            row = cursor.fetchone()
            if row:
                return {
                    'Id': row[0],
                    'Username': row[1],
                    'Password': row[2],
                    'CreatedOn': row[3]
                }
            return None  # If no user found, return None
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving the user: {e}")
            return None

class ToDoModel:
    TABLENAME = "Todo"

    def __init__(self):
        # Initialize the connection to the database
        self.conn = sqlite3.connect('app.db')

    def __del__(self):
        # Ensure that the connection is closed
        self.conn.commit()
        self.conn.close()

    def create(self, params):
        query = f'INSERT INTO {self.TABLENAME} (Title, Description, DueDate, UserId) VALUES (?, ?, ?, ?)'
        cursor = self.conn.cursor()  # Create a cursor object to execute the query
        cursor.execute(query, (params["Title"], params["Description"], params["DueDate"], params["UserId"]))
        self.conn.commit()  # Commit the transaction
        return self.get_by_id(cursor.lastrowid)  # Use cursor.lastrowid

    def get_all(self, user_id):
        query = f'SELECT * FROM {self.TABLENAME} WHERE UserId = ?'
        return self.conn.execute(query, (user_id,)).fetchall()

    def get_by_id(self, todo_id):
        query = f'SELECT * FROM {self.TABLENAME} WHERE id = ?'
        return self.conn.execute(query, (todo_id,)).fetchone()
    
    def delete(self, item_id):
        cursor = self.conn.cursor()
        try:
            query = f'DELETE FROM {self.TABLENAME} where id = {item_id}'
            self.conn.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error deleting todo: {e}")
            return False
        finally:
            cursor.close()

    def update(self, item_id, params):
        cursor = self.conn.cursor()
        try:
            query = f'UPDATE {self.TABLENAME} SET Title = ?, Description = ?, DueDate = ? WHERE id = ?'
            cursor.execute(query, (params["Title"], params["Description"], params["DueDate"], item_id))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error updating todo: {e}")
            return False
        finally:
            cursor.close()