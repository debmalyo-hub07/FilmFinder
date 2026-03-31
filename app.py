import streamlit as st
import pickle
from src.ui.home import show_home_page
from src.ui.details import show_movie_details
from src.utils.styling import apply_custom_css

# Page config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load movie dataset & similarity model
with open("model/movie_list.pkl", "rb") as f:
    movies = pickle.load(f)

with open("model/similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

def main():
    apply_custom_css()

    query_params = st.query_params
    page = query_params.get("page", "home")
    movie_id = query_params.get("movie_id", None)

    if page == "details" and movie_id:
        show_movie_details(int(movie_id))
    else:
        show_home_page(movies, similarity)

if __name__ == "__main__":
    main()
