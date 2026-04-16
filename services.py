import requests
import os

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

def buscar_filmes_populares():
    # Busca filmes populares em português [cite: 29]
    url = f"{BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=pt-BR"
    response = requests.get(url)
    
    if response.status_code == 200:
        movies_data = response.json().get('results', [])
        # Formatamos para facilitar o uso no Flutter e no Banco [cite: 28]
        return [{
            "id": str(m['id']),
            "title": m['title'],
            "poster_url": f"https://image.tmdb.org/t/p/w500{m['poster_path']}",
            "overview": m['overview'],
            "release_year": int(m['release_date'][:4]) if m['release_date'] else None,
            "rating": m['vote_average']
        } for m in movies_data]
    return []