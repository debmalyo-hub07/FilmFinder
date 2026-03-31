import streamlit as st
import time
from src.recommender.engine import recommend
from src.utils.styling import create_recommendations_grid_streamlit, create_home_header
from src.utils.tmdb import fetch_poster

import concurrent.futures

def fetch_movie_poster_safe(row):
    """Isolated worker for single TMDB call"""
    movie_id = next((row[k] for k in ['id', 'movie_id', 'tmdb_id', 'movieId'] if k in row), None)
    title = next((row[k] for k in ['title', 'Title', 'original_title', 'movie_title'] if k in row), "Unknown")
    
    try:
        poster_url = fetch_poster(movie_id) if movie_id else ""
        return {'id': movie_id, 'title': title, 'poster': poster_url}
    except Exception:
        return {'id': movie_id, 'title': title, 'poster': ''}

def get_random_trending_movies(movies_df, num_movies=10):
    """
    Safely curates a random list of 10 movies for the Prime Discover feed.
    Uses 5 parallel workers to reduce load time from ~4 seconds to ~0.5 seconds safely.
    """
    sampled = movies_df.sample(n=num_movies).to_dict('records')
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_movie_poster_safe, row): row for row in sampled}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
    return results

def show_home_page(movies, similarity):
    # ===========================
    # PREMIUM HEADER SECTION
    # ===========================
    st.markdown(create_home_header(), unsafe_allow_html=True)
    
    # Initialize Trending Movies exactly ONCE securely.
    if "trending_movies" not in st.session_state or len(st.session_state.trending_movies) < 10:
        with st.spinner("Curating your Discover feed..."):
            st.session_state.trending_movies = get_random_trending_movies(movies, 10)

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
                time.sleep(0.5) 
                
                try:
                    raw_recommendations = recommend(selected_movie, movies, similarity)
                except ValueError as ve:
                    st.toast(str(ve), icon="⚠️")
                    raw_recommendations = []
                except Exception as e:
                    st.toast("Fatal AI Error while computing matrix.", icon="🚨")
                    raw_recommendations = []

                processed_recommendations = []

                for i, movie in enumerate(raw_recommendations):
                    try:
                        movie_id = next((movie[k] for k in ['id', 'movie_id', 'tmdb_id', 'movieId'] if k in movie), i)
                        title = next((movie[k] for k in ['title', 'Title', 'original_title', 'movie_title'] if k in movie and movie[k]), f"Unknown Movie {i}")
                        poster_url = next((movie[k] for k in ['poster', 'poster_url', 'poster_path', 'Poster'] if k in movie and movie[k]), "")

                        processed_recommendations.append({
                            'id': movie_id,
                            'title': title,
                            'poster': poster_url
                        })
                    except Exception as e:
                        pass # Ignore silent errors on specific cards
                
                # Write to Session State
                st.session_state.recommended_movies = processed_recommendations
                
    st.markdown('</div>', unsafe_allow_html=True)

    # ===========================
    # DISPLAY STUNNING RESULTS
    # ===========================
    
    # Check if we have active searched recommendations loaded
    if "recommended_movies" in st.session_state and len(st.session_state.recommended_movies) > 0:
        st.markdown('<div class="recommendations-title">Matches You Will Love</div>', unsafe_allow_html=True)
        try:
            create_recommendations_grid_streamlit(st.session_state.recommended_movies)
            st.toast("Recommendations injected perfectly!", icon="✨")
        except Exception as e:
            st.error("Failed to render the cinematic grid safely.", icon="🚨")
            
    # Default State: Show Discover Prime Picks if there's no active search payload
    else:
        st.markdown(
            '<div class="recommendations-title" style="margin-top: 1rem;">🔥 Discover Prime Picks</div>', 
            unsafe_allow_html=True
        )
        try:
            create_recommendations_grid_streamlit(st.session_state.trending_movies)
        except Exception as e:
            st.error(f"Trending Render Error: {e}")

    # ===========================
    # DEVELOPER FOOTER
    # ===========================
    st.markdown("""
        <div style="text-align:center; padding-top:40px; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.05); color: var(--text-muted); font-size: 0.95rem;">
            <div style="margin-bottom: 12px;">© 2026 FilmFinder &bull; Crafted with passion for cinema by <b style="color: var(--text-primary);">Rajdeep Biswas</b></div>
            <div style="display: flex; justify-content: center; gap: 20px; align-items: center; margin-top: 15px;">
                <a href="mailto:brajdeep029@gmail.com" title="Email" target="_blank" rel="noopener noreferrer" style="color: var(--text-muted); transition: color 0.3s;" onmouseover="this.style.color='#ea4335'" onmouseout="this.style.color='var(--text-muted)'">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                </a>
                <a href="https://www.facebook.com/rajdeep.biswas.14203/" title="Facebook" target="_blank" rel="noopener noreferrer" style="color: var(--text-muted); transition: color 0.3s;" onmouseover="this.style.color='#1877f2'" onmouseout="this.style.color='var(--text-muted)'">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
                </a>
                <a href="https://www.instagram.com/rajdeepbiswas_01/?hl=en" title="Instagram" target="_blank" rel="noopener noreferrer" style="color: var(--text-muted); transition: color 0.3s;" onmouseover="this.style.color='#E1306C'" onmouseout="this.style.color='var(--text-muted)'">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
