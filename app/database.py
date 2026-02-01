import sqlite3

# Establish a connection to the SQLite database
connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# creating a table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS shipments(
    id INTEGER, 
    content TEXT,
    weight REAL, 
    status TEXT)"""
)
# Closing the connection
connection.close()
