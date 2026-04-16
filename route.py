from flask import jsonify, request
from app import app
from models import db, Usuario, Filme, Swipe, Match
from services import buscar_filmes_populares

@app.route('/filmes/feed', methods=['GET'])
def get_feed_filmes():
    # Por enquanto, busca direto da API para testar o Swipe [cite: 28]
    filmes = buscar_filmes_populares()
    return jsonify(filmes), 200

@app.route('/swipe', methods=['POST'])
def registrar_swipe():
    data = request.json
    # Criamos o registro do swipe conforme seu modelo
    novo_swipe = Swipe(
        user_id=data.get('user_id'),
        movie_id=data.get('movie_id'),
        session_id=data.get('session_id'),
        direction=data.get('direction') # 'like' ou 'dislike'
    )
    db.session.add(novo_swipe)
    db.session.commit()
    
    # Lógica simples de Match Engine sugerida [cite: 29]
    if data.get('direction') == 'like':
        # Verifica se alguém mais na sessão deu like neste filme
        outros_likes = Swipe.query.filter_by(
            movie_id=data.get('movie_id'),
            session_id=data.get('session_id'),
            direction='like'
        ).count()
        
        if outros_likes > 1:
            return jsonify({"status": "match", "message": "Temos um Match!"}), 201
            
    return jsonify({"status": "success"}), 201