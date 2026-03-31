import requests

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_poster(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        data = requests.get(url).json()
        return "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")
    except:
        return ""

def fetch_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        movie_data = requests.get(url).json()
    except Exception:
        return None

    credits_url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
    try:
        credits_data = requests.get(credits_url).json()
    except:
        credits_data = {}

    videos_url = f"{BASE_URL}/movie/{movie_id}/videos?api_key={API_KEY}"
    try:
        videos_data = requests.get(videos_url).json()
        # Find Official Trailer or at least a YouTube video
        trailer_key = next((v['key'] for v in videos_data.get('results', []) if v['site'] == 'YouTube' and v['type'] == 'Trailer'), None)
        if not trailer_key and videos_data.get('results'):
             trailer_key = next((v['key'] for v in videos_data.get('results') if v['site'] == 'YouTube'), None)
    except:
        trailer_key = None

    director = next((p["name"] for p in credits_data.get("crew", []) if p["job"] == "Director"), "N/A")
    cast = [p["name"] for p in credits_data.get("cast", [])[:5]]
    genres = [g["name"] for g in movie_data.get("genres", [])]
    companies = [c["name"] for c in movie_data.get("production_companies", [])[:3]]

    # Formatter for financials
    budget = movie_data.get("budget", 0)
    revenue = movie_data.get("revenue", 0)
    
    def format_money(amount):
        if not amount or amount == 0:
            return "Unknown"
        if amount >= 1_000_000_000:
            return f"${amount / 1_000_000_000:.1f}B"
        if amount >= 1_000_000:
            return f"${amount / 1_000_000:.1f}M"
        return f"${amount:,}"

    return {
        "title": movie_data.get("title", "N/A"),
        "tagline": movie_data.get("tagline", ""),
        "overview": movie_data.get("overview", "No overview available."),
        "poster_path": "https://image.tmdb.org/t/p/w500/" + movie_data.get("poster_path", "") if movie_data.get("poster_path") else "",
        "backdrop_path": "https://image.tmdb.org/t/p/w1280/" + movie_data.get("backdrop_path", "") if movie_data.get("backdrop_path") else "",
        "director": director,
        "cast": cast,
        "genres": genres,
        "release_date": movie_data.get("release_date", "N/A"),
        "runtime": movie_data.get("runtime", "N/A"),
        "vote_average": movie_data.get("vote_average", "N/A"),
        "status": movie_data.get("status", "Released"),
        "budget": format_money(budget),
        "revenue": format_money(revenue),
        "companies": companies,
        "trailer_key": trailer_key
    }
