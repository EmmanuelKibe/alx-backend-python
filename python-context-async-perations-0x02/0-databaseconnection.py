import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open the connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor   # return cursor so we can execute queries

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes if no error
        if exc_type is None:
            self.conn.commit()
        else:
            # Rollback if there's an error
            self.conn.rollback()

        # Close connection
        self.conn.close()

        return False

# Using the context manager to run a query
with DatabaseConnection("my_database.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()

print(results)

