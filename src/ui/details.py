import streamlit as st
from src.utils.tmdb import fetch_movie_details

def show_movie_details(movie_id):
    # Back button navigation
    st.markdown('<div class="details-topbar">', unsafe_allow_html=True)
    if st.button("← Back to recommendations", key="back_btn"):
        st.query_params.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    with st.spinner("Preparing the theater..."):
        movie_details = fetch_movie_details(movie_id)

    if not movie_details:
        st.toast("Network failure: External API dropped the connection.", icon="📉")
        st.error("Unable to load movie details. The reels might be missing!", icon="❌")
        return

    # Extract dynamic properties
    title = movie_details.get("title", "Unknown")
    tagline = movie_details.get("tagline", "")
    overview = movie_details.get("overview", "No synopsis available.")
    rating = movie_details.get("vote_average", "N/A")
    runtime = movie_details.get("runtime", "N/A")
    status = movie_details.get("status", "Released")
    budget = movie_details.get("budget", "Unknown")
    revenue = movie_details.get("revenue", "Unknown")
    year = movie_details.get("release_date", "N/A")[:4] if movie_details.get("release_date") else "N/A"
    genres = ", ".join(movie_details.get("genres", []))
    director = movie_details.get("director", "Unknown")
    cast = ", ".join(movie_details.get("cast", []))
    companies = ", ".join(movie_details.get("companies", []))
    backdrop = movie_details.get("backdrop_path", "")
    poster = movie_details.get("poster_path", "")
    trailer_key = movie_details.get("trailer_key", None)

    # Clean rating display
    if isinstance(rating, (int, float)):
        rating_ui = f"{rating:.1f}"
    else:
        rating_ui = "N/A"

    # Cinematic Hero Section
    if backdrop:
        st.markdown(f"""
<div class="details-hero">
<img src="{backdrop}" alt="Backdrop">
<div class="details-gradient"></div>
</div>
""", unsafe_allow_html=True)

    # Content Row (Poster + Information)
    st.markdown('<div class="details-content-row page-animate">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2.8], gap="large")

    with col1:
        fallback = f"https://via.placeholder.com/500x750/19222C/FFFFFF?text={title.replace(' ', '+')}"
        effective_poster = poster if poster and not "None" in poster else fallback
        st.markdown(f"""
<img src="{effective_poster}" class="details-poster" alt="{title} Poster">
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f'<h1 class="details-title">{title}</h1>', unsafe_allow_html=True)
        
        if tagline:
            st.markdown(f'<div class="details-tagline">"{tagline}"</div>', unsafe_allow_html=True)
        
        # Meta info row
        st.markdown(f"""
<div class="details-meta">
<span class="meta-rating">★ {rating_ui}</span>
<span class="meta-pill">{year}</span>
<span class="meta-pill">{runtime} min</span>
<span class="meta-pill">{status}</span>
<span class="meta-pill" style="color: var(--accent);">{genres}</span>
</div>
""", unsafe_allow_html=True)

        # Crew Overview
        st.markdown(f"""
<div class="crew-grid">
<div class="crew-box">
<div class="crew-label">Director</div>
<div class="crew-value">{director}</div>
</div>
<div class="crew-box">
<div class="crew-label">Top Cast</div>
<div class="crew-value" style="font-size: 0.95rem; font-weight: 500;">{cast}</div>
</div>
<div class="crew-box">
<div class="crew-label">Studios</div>
<div class="crew-value" style="font-size: 0.95rem; font-weight: 500;">{companies if companies else 'Indie/Unknown'}</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Overview & Financials Box Container
    st.markdown(f"""
<div class="overview-box page-animate" style="animation-delay: 0.2s;">
<h3>Synopsis</h3>
<p>{overview}</p>
<div class="financial-grid">
<div class="financial-col">
<span class="financial-label">Budget</span>
<span class="financial-value">{budget}</span>
</div>
<div class="financial-col">
<span class="financial-label">Box Office</span>
<span class="financial-value">{revenue}</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Trailer Section
    if trailer_key:
        st.markdown(f"""
<div class="overview-box page-animate" style="animation-delay: 0.4s; margin-top: 2rem;">
<h3>Official Trailer</h3>
<div class="trailer-container">
<iframe src="https://www.youtube.com/embed/{trailer_key}?autoplay=0&rel=0" 
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
allowfullscreen>
</iframe>
</div>
</div>
""", unsafe_allow_html=True)