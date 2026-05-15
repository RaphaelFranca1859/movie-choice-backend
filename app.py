from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import requests
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

DATABASE = "database.db"
# 🔑 CHAVE CORRIGIDA AQUI
TMDB_API_KEY = "293829bce045198e098031b1fb95551c"
BASE_URL = "https://api.themoviedb.org/3"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, 
        display_name TEXT, avatar_url TEXT, created_at TEXT, last_login TEXT
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS filmes (
        id TEXT PRIMARY KEY, title TEXT, poster_url TEXT, 
        overview TEXT, release_year INTEGER, rating REAL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS swipes (
        id TEXT PRIMARY KEY, user_id TEXT, movie_id TEXT, 
        session_id TEXT, direction TEXT, swiped_at TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

def buscar_filmes_populares():
    # Busca do TMDB usando a chave fixa
    url = f"{BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=pt-BR"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            movies = response.json().get('results', [])
            return [{
                "id": str(m['id']),
                "title": m['title'],
                "poster_url": f"https://image.tmdb.org/t/p/w500{m['poster_path']}",
                "overview": m['overview'],
                "release_year": int(m['release_date'][:4]) if m['release_date'] else None,
                "rating": m['vote_average']
            } for m in movies]
    except Exception as e:
        print(f"Erro na API: {e}")
    return []

# --- ROTAS PRINCIPAIS ---

@app.route('/filmes/feed', methods=['GET'])
def get_filmes():
    filmes = buscar_filmes_populares()
    return jsonify(filmes), 200

@app.route('/swipe', methods=['POST'])
def swipe():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    swipe_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO swipes VALUES (?, ?, ?, ?, ?, ?)", 
        (swipe_id, data.get('user_id'), data.get('movie_id'), 
         data.get('session_id'), data.get('direction'), datetime.utcnow().isoformat()))
    conn.commit()
    
    match = False
    if data.get('direction') == 'like':
        cursor.execute("SELECT COUNT(*) as total FROM swipes WHERE movie_id = ? AND session_id = ? AND direction = 'like'", 
                       (data.get('movie_id'), data.get('session_id')))
        if cursor.fetchone()["total"] > 1: match = True
            
    conn.close()
    return jsonify({"status": "success", "match": match}), 201

# --- ROTAS PARA TESTAR CRUD (Controle de Usuários) ---

@app.route('/usuarios', methods=['GET', 'POST'])
def crud_usuarios():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST': # CREATE
        data = request.json
        user_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO usuarios (id, email, password_hash, display_name) VALUES (?, ?, ?, ?)",
                       (user_id, data['email'], "1234", data['nome']))
        conn.commit()
        conn.close()
        return jsonify({"id": user_id, "message": "Criado"}), 201
    
    # READ
    cursor.execute("SELECT * FROM usuarios")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/usuarios/<id>', methods=['DELETE'])
def deletar_usuario(id): # DELETE
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deletado"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)