import sqlite3

connection = None

try:
    connection = sqlite3.connect('censoescolar.db')

    with open('schema.sql') as file:
        connection.executescript(file.read())

    connection.commit()
except sqlite3.Error as e:
    print(f'O sqlite lançou uma exceção: {str(e)}')
finally:
    if connection is not None:
        connection.close()
