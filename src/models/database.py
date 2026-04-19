```python
import sqlite3
from typing import List, Dict

class Database:
    def __init__(self, db_name: str):
        """
        Initialize the database connection.

        Args:
        db_name (str): The name of the database file.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self, table_name: str, columns: List[Dict]):
        """
        Create a new table in the database.

        Args:
        table_name (str): The name of the table to create.
        columns (List[Dict]): A list of dictionaries containing column information.
        """
        try:
            column_defs = ", ".join([f"{col['name']} {col['type']}" for col in columns])
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, table_name: str, data: List[Dict]):
        """
        Insert data into a table.

        Args:
        table_name (str): The name of the table to insert into.
        data (List[Dict]): A list of dictionaries containing data to insert.
        """
        try:
            placeholders = ", ".join(["?"] * len(data[0]))
            self.cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", [list(row.values()) for row in data])
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
```