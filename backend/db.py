from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE_FILE = './database/database.db'


def create_database_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create the table to store database information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS databases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            idowner INTEGER,
            datacreation DATE,
            datamodification DATE
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            iddb INTEGER,
            name TEXT,           
            datacreation DATE,
            datamodification DATE
        )
    ''')

    conn.commit()
    conn.close()



def create_table_(database_name, table_name, table_attributes):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create the table with the provided table attributes
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {table_attributes}
        )
    ''')

    conn.commit()
    conn.close()

  


@app.route('/create-database', methods=['POST'])
def create_database():
    data = request.get_json()
    database_name = data['databasename']
    print(database_name)     

    # Create a new database file
    new_database_file = f'{database_name}.db'
    open(f'./database/{new_database_file}', 'w').close()

    # Add a line to the main database table
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO databases (name, idowner, datacreation, datamodification)
        VALUES (?, ?, DATE('now'), DATE('now'))
    ''', (database_name, data['idowner']))

    conn.commit()
    conn.close()

    return jsonify({'message': f'Database "{database_name}" created successfully.'})


@app.route('/create-table', methods=['POST'])
def create_table():
    data = request.get_json()
    database_id = data['dbid']
    table_name = data['tablename']
    table_attributes = data['table_attributes']

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM databases WHERE id="+str(database_id))
    database_name = cursor.fetchall()    
    cursor.execute('''
        INSERT INTO databases (name, idowner, datacreation, datamodification)
        VALUES (?, ?, DATE('now'), DATE('now'))
    ''', (table_name, database_id))

    # Create the table in the specified database with the provided table attributes
    create_table_(f'{database_name}.db', table_name, table_attributes)

    return jsonify({'message': f'Table "{table_name}" created successfully in database "{database_name}".'})

@app.route('/get_databases', methods=['GET'])
def get_databases():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM databases')
    databases = cursor.fetchall()

    conn.close()

    return jsonify({'databases': databases})


@app.route('/get_tables', methods=['GET'])
def get_tables():
    data = request.get_json()
    database_id = data['dbid']

    if not database_id:
        return jsonify({'message': 'Please provide the database_id parameter.'}), 400
    cursor.execute("SELECT name FROM databases WHERE id="+str(database_id))
    database_name = cursor.fetchall()  
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM tables WHERE iddb="+str())
    tables = cursor.fetchall()

    conn.close()

    return jsonify({'tables': tables})

if __name__ == '__main__':
    create_database_table()
    app.run(debug=True)
