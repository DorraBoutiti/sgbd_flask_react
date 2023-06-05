from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
db_path = './database/database.db'

# Fetch user's databases
@app.route('/databases', methods=['GET'])
def fetch_databases():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM databases')
    result = cursor.fetchall()

    conn.close()

    return jsonify(result)

# Create a new database
@app.route('/databases', methods=['POST'])
def create_database():
    data = request.get_json()
    name = data['name']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO databases (name) VALUES (?)', (name,))
    conn.commit()

    database_id = cursor.lastrowid

    conn.close()

    return jsonify({'id': database_id, 'name': name})

# Fetch tables in a database
@app.route('/databases/<int:database_id>/tables', methods=['GET'])
def fetch_tables(database_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tables WHERE database_id = ?', (database_id,))
    result = cursor.fetchall()

    conn.close()

    return jsonify(result)

# Insert data into a table
@app.route('/tables/<int:table_id>/data', methods=['POST'])
def insert_data(table_id):
    data = request.get_json()
    values = tuple(data.values())

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    placeholders = ', '.join(['?'] * len(data))
    query = f'INSERT INTO table{table_id} ({", ".join(data.keys())}) VALUES ({placeholders})'
    cursor.execute(query, values)
    conn.commit()

    data_id = cursor.lastrowid

    conn.close()

    return jsonify({'id': data_id, **data})

# Fetch all data from a table
@app.route('/tables/<int:table_id>/data', methods=['GET'])
def fetch_table_data(table_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM table{table_id}')
    result = cursor.fetchall()

    conn.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
