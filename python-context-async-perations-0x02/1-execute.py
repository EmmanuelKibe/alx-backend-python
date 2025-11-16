import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open DB connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Execute the query
        self.cursor.execute(self.query, self.params)

        # Fetch results
        self.results = self.cursor.fetchall()

        # Return results directly
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit only if no error
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        # Close the connection
        self.conn.close()

        # Returning False means errors (if any) should not be suppressed
        return False

query = "SELECT * FROM users WHERE age > ?"

with ExecuteQuery("my_database.db", query, (25,)) as results:
    print(results)
