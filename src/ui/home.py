import streamlit as st
import time
from src.recommender.engine import recommend
from src.utils.styling import create_recommendations_grid_streamlit, create_home_header

def show_home_page(movies, similarity):
    # ===========================
    # PREMIUM HEADER SECTION
    # ===========================
    st.markdown(create_home_header(), unsafe_allow_html=True)

    # ===========================
    # DYNAMIC SEARCH COMPONENT
    # ===========================
    st.markdown('<div class="search-section">', unsafe_allow_html=True)
    
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        label="Search Movie",
        options=movie_list,
        index=None,
        placeholder="🔍 Type a movie title to discover similar gems...",
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ===========================
    # PRIMARY CTA BUTTON
    # ===========================
    st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
    if st.button("✨ Get Personalized Recommendations", use_container_width=True):
        if not selected_movie or selected_movie.strip() == "":
            st.warning("Please select a movie first to unlock your recommendations. 🎬")
        else:
            with st.spinner("Analyzing cinematic patterns..."):
                # Minor deliberate delay to make it feel like intensive AI work
                time.sleep(0.5) 
                
                raw_recommendations = recommend(selected_movie, movies, similarity)

                processed_recommendations = []

                for i, movie in enumerate(raw_recommendations):
                    try:
                        # Extract universal identifiers seamlessly
                        movie_id = next((movie[k] for k in ['id', 'movie_id', 'tmdb_id', 'movieId'] if k in movie), i)
                        title = next((movie[k] for k in ['title', 'Title', 'original_title', 'movie_title'] if k in movie and movie[k]), f"Unknown Movie {i}")
                        poster_url = next((movie[k] for k in ['poster', 'poster_url', 'poster_path', 'Poster'] if k in movie and movie[k]), "")

                        processed_recommendations.append({
                            'id': movie_id,
                            'title': title,
                            'poster': poster_url
                        })

                    except Exception as e:
                        print(f"Error processing movie {i}: {e}") # Log silently

                st.session_state.recommended_movies = processed_recommendations
                
    st.markdown('</div>', unsafe_allow_html=True)

    # ===========================
    # DISPLAY STUNNING RESULTS
    # ===========================
    if "recommended_movies" in st.session_state and len(st.session_state.recommended_movies) > 0:
        st.markdown('<div class="recommendations-title">Matches You Will Love</div>', unsafe_allow_html=True)

        try:
            create_recommendations_grid_streamlit(st.session_state.recommended_movies)
        except Exception as e:
            st.error(f"Render Error: {e}")

    # ===========================
    # MINIMALIST FOOTER
    # ===========================
    st.markdown("""
        <div style="text-align:center; padding-top:40px; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.05); color: var(--text-muted); font-size: 0.9rem;">
            © 2026 FilmFinder • Crafted with passion for cinema.
        </div>
    """, unsafe_allow_html=True)
