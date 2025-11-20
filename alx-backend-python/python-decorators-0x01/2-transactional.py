import sqlite3 
import functools
from . import with_db_connection, transactional

#### decorator to handle transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Begin a transaction
            conn.execute('BEGIN')
            result = func(conn, *args, **kwargs)
            
            # Commit the transaction if successful
            conn.commit()
            return result
        except Exception as e:
            # Rollback the transaction in case of error
            conn.rollback()
            raise e
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')