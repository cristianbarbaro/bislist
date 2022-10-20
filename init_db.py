import sqlite3

connection = sqlite3.connect('app/db/database.sqlite3')


with open('app/scripts/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()