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

@st.cache_resource(show_spinner="Booting Cinematic AI Engine...")
def load_data():
    try:
        with open("model/movie_list.pkl", "rb") as f:
            m = pickle.load(f)
        with open("model/similarity.pkl", "rb") as f:
            s = pickle.load(f)
        return m, s
    except Exception as e:
        return None, None

movies, similarity = load_data()

# Halt application completely if primary datasets are fatally missing
if movies is None or similarity is None:
    apply_custom_css() # Keep standard black UI
    st.error("### 🚨 Critical System Error\nMachine Learning models failed to load. Please ensure `model/movie_list.pkl` and `model/similarity.pkl` are present.", icon="❌")
    st.stop()

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
