import os
import sqlite3

from sqlite3 import Connection, Cursor

class TransactionHandler:
    connection: Connection

    # Called when entering the context
    # Establishes a connection with the db and returns a Cursor object
    def __enter__(self) -> Cursor:
        cwd = os.getcwd()
        relativePath = "dao/db/rubble_rescue.db"
        targetPath = os.path.join(cwd, relativePath)
        
        self.connection = sqlite3.connect(targetPath)
        return self.connection.cursor()
    
    # Called when exiting the context
    # If no exception occurs during the transaction, the changes are committed, else is rolled back
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        
        self.connection.close()
