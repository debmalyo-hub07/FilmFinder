import streamlit as st

def apply_custom_css():
    """Apply custom CSS with proper encoding handling"""
    # Hide Streamlit default UI elements early
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

    try:
        with open("src/utils/style.css", "r", encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load CSS: {e}")

def create_movie_card_streamlit(movie_id, title, poster_url):
    """Create a strictly aligned movie card using Streamlit components for proper navigation"""
    
    # We create the visual card purely in HTML/CSS
    # The title height is fixed by CSS, poster aspect ratio is fixed by CSS hack.
    # The 'btn-details' acts as a visual anchor.
    # We use Streamlit's native button logic implicitly by rendering an <a> tag targeting query params.
    
    details_url = f"?page=details&movie_id={movie_id}"
    
    html = f"""
    <div class="movie-card-wrapper">
        <div class="poster-container">
            <img src="{poster_url}" alt="{title}" loading="lazy" onerror="this.src='https://via.placeholder.com/500x750/111111/FFFFFF?text=No+Poster'">
        </div>
        <div class="card-content">
            <div class="card-title" title="{title}">{title}</div>
            <a href="{details_url}" target="_self" class="btn-details">
                Show Details
            </a>
        </div>
    </div>
    """
    
    # Render with Streamlit
    st.markdown(html, unsafe_allow_html=True)

def create_recommendations_grid_streamlit(movies):
    """Create a robust column-based grid for recommendations"""
    if not movies or len(movies) == 0:
        st.warning("No movies found to display.")
        return None

    # Determine number of columns based on standard layouts
    num_cols = min(5, len(movies))
    cols = st.columns(num_cols, gap="medium")
    
    clicked_movie_id = None

    for idx, movie in enumerate(movies[:num_cols]):
        movie_id = movie.get('id', idx)
        title = movie.get('title', 'Unknown Title')
        poster_url = movie.get('poster', '')
        
        # Ensure we always have a poster structure
        if not poster_url:
            poster_url = f"https://via.placeholder.com/500x750/19222C/FFFFFF?text={title.replace(' ', '+')}"

        with cols[idx]:
            # This renders the card HTML. 
            # We rely on the absolute perfectly sized CSS elements inside it so columns don't jitter
            create_movie_card_streamlit(movie_id, title, poster_url)

    return clicked_movie_id

def create_home_header():
    """Create an elegant Home banner"""
    return """
    <div class="hero-header">
        <h1 class="hero-title">
            <span>Movie</span> Recommender
        </h1>
        <p class="hero-subtitle">Your cinematic journey begins here. Powered by cutting-edge AI, discover your next favorite movie.</p>
    </div>
    """

def create_search_section():
    """Search Header spacing"""
    return ""  # Handled natively via Streamlit selectbox padding
