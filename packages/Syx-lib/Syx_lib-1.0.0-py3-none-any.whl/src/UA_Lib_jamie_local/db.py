import json
import os
import sqlite3

class UADatabase:
    def __init__(self, filename):
        if not filename.endswith(('.ua', '.hdb')):
            raise ValueError("Unsupported file extension. Use '.ua' or '.hdb'")
        self.filename = filename
        self.data = {}
        self.is_connected = False

    def connect_db(self):
        """Simulates opening a connection to the database."""
        if self.is_connected:
            print("Database is already connected.")
            return

        # Load the data when connecting
        self.load()
        self.is_connected = True
        print("Connected to the database.")

    def disconnect_db(self):
        """Simulates closing the connection to the database."""
        if not self.is_connected:
            print("Database is not connected.")
            return

        # Save the data before disconnecting
        self.save()
        self.is_connected = False
        print("Disconnected from the database.")

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)

    def save(self):
        if self.is_connected:
            with open(self.filename, 'w') as file:
                json.dump(self.data, file, indent=4)

    def add_entry(self, key, value):
        if not self.is_connected:
            raise RuntimeError("Database is not connected.")
        self.data[key] = value
        self.save()

    def get_entry(self, key):
        if not self.is_connected:
            raise RuntimeError("Database is not connected.")
        return self.data.get(key, None)

    def update_entry(self, key, value):
        if not self.is_connected:
            raise RuntimeError("Database is not connected.")
        if key in self.data:
            self.data[key] = value
            self.save()
            return True
        return False

    def delete_entry(self, key):
        if not self.is_connected:
            raise RuntimeError("Database is not connected.")
        if key in self.data:
            del self.data[key]
            self.save()
            return True
        return False

    def get_all(self):
        """Retrieves all entries from the database."""
        if not self.is_connected:
            raise RuntimeError("Database is not connected.")
        return self.data

    @staticmethod
    def create_database(filename):
        if not filename.endswith(('.ua', '.hdb')):
            raise ValueError("Unsupported file extension. Use '.ua' or '.hdb'")
        with open(filename, 'w') as file:
            json.dump({}, file, indent=4)
        return UADatabase(filename)

    @staticmethod
    def convert_sqlite(sqlite_file, ua_filename):
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # Get all tables in the SQLite database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        ua_db = UADatabase.create_database(ua_filename)

        for table_name in tables:
            table_name = table_name[0]
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]

            # Store each row as a dictionary
            for row in rows:
                entry = dict(zip(columns, row))
                ua_db.connect_db()
                ua_db.add_entry(f"{table_name}_{row[0]}", entry)  # Assuming the first column is a unique ID

        conn.close()
        ua_db.disconnect_db()
        return ua_db
