from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

# 1. Tabela de Usuários
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

# 2. Tabela de Grupos
class Grupo(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    invite_code = db.Column(db.String(10), unique=True)
    created_by = db.Column(db.String, db.ForeignKey('usuarios.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

# 3. Tabela de Filmes (Cache local dos dados do TMDB)
class Filme(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.String, primary_key=True) # Usaremos o ID do TMDB
    title = db.Column(db.String(255), nullable=False)
    poster_url = db.Column(db.String(500))
    overview = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    genres = db.Column(db.String(255))
    rating = db.Column(db.Float)

class Secao(db.Model):
    __tablename__ = 'secoes'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = db.Column(db.String, db.ForeignKey('grupos.id'))
    mode = db.Column(db.String(50)) # Ex: 'Normal' ou 'Blind Box'
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
# 4. Tabela de Swipes (Onde a mágica acontece)
class Swipe(db.Model):
    __tablename__ = 'swipes'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String, db.ForeignKey('secoes.id'))
    user_id = db.Column(db.String, db.ForeignKey('usuarios.id'))
    movie_id = db.Column(db.String, db.ForeignKey('filmes.id'))
    direction = db.Column(db.String(10)) # 'like' ou 'dislike'
    swiped_at = db.Column(db.DateTime, default=datetime.utcnow)

# 5. Tabela de Matches
class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String, db.ForeignKey('secoes.id'))
    movie_id = db.Column(db.String, db.ForeignKey('filmes.id'))
    matched_at = db.Column(db.DateTime, default=datetime.utcnow)
    match_count = db.Column(db.Integer, default=1)