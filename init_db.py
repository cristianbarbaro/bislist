import sqlite3

connection = sqlite3.connect('db/database.sqlite3')


with open('scripts/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()