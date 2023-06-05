from flask import Flask, request, jsonify
from flask_cors import CORS

import sqlite3

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")
db_path = './database/users.db'
def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES utilisateurs (id)
        )
    ''')

    conn.commit()
    conn.close()

# Fonction pour charger des données initiales dans la table Utilisateurs
def charger_donnees_initiales():
    utilisateurs = [
        ('Alice', '123456'),
        ('Bob', 'abcdef'),
        ('Charlie', 'password123')
    ]

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.executemany('INSERT INTO utilisateurs (username, password) VALUES (?, ?)', utilisateurs)
        conn.commit()

# Création de la base de données
create_database()
# Fonction pour ajouter un utilisateur
@app.route('/utilisateurs', methods=['POST'])
def ajouter_utilisateur():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO utilisateurs (username, password) VALUES (?, ?)', (username, password))
        user_id = cur.lastrowid
        cur.execute('INSERT INTO credentials (user_id, username, password) VALUES (?, ?, ?)', (user_id, username, password))
        
        conn.commit()
    
    return jsonify({'message': 'Utilisateur ajouté avec succès'})

# Fonction pour obtenir tous les utilisateurs
@app.route('/utilisateurs', methods=['GET'])
def obtenir_utilisateurs():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM utilisateurs')
        utilisateurs = cur.fetchall()
    
    result = []
    for utilisateur in utilisateurs:
        result.append({
            'id': utilisateur[0],
            'username': utilisateur[1],
            'password': utilisateur[2]
        })
    
    return jsonify(result)

# Fonction pour mettre à jour l'âge d'un utilisateur
@app.route('/utilisateurs/<int:utilisateur_id>', methods=['PUT'])
def mettre_a_jour_password_utilisateur(utilisateur_id):
    data = request.get_json()
    nouvel_password = data['password']
    
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE utilisateurs SET password = ? WHERE id = ?', (nouvel_password, utilisateur_id))
        conn.commit()
    
    return jsonify({'message': 'Mot de passe de l\'utilisateur mis à jour avec succès'})

# Fonction pour supprimer un utilisateur
@app.route('/utilisateurs/<int:utilisateur_id>', methods=['DELETE'])
def supprimer_utilisateur(utilisateur_id):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM utilisateurs WHERE id = ?', (utilisateur_id,))
        conn.commit()
    
    return jsonify({'message': 'Utilisateur supprimé avec succès'})
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM credentials WHERE username = ? AND password = ?', (username, password))
        result = cur.fetchone()

        if result:
            user_id = result[1]  # Récupérer l'ID de l'utilisateur associé
            return jsonify({'message': 'Authentification réussie', 'user_id': user_id})
        else:
            return jsonify({'message': 'Échec de l\'authentification'})

if __name__ == '__main__':
    app.run(debug=True)
