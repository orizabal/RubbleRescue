import sqlite3

connection = sqlite3.connect("RubbleRescue.db")
print(connection.total_changes)