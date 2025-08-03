import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
import subprocess

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.models import Article

# ----- Custom CSS Styling -----
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
    }
    .news-card {
        background-color: white;
        padding: 20px;
        margin: 10px 0;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Setup DB connection (DO NOT keep session global)
engine = create_engine('sqlite:///news.db')

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

st.title("📰 News Aggregator Dashboard")

# Refresh Button
if st.button("🔄 Refresh News"):
    with st.spinner("Fetching latest news..."):
        subprocess.run(["python", "scrapers/newsapi_scraper.py"])
    st.experimental_rerun()

# Create a new session every time the page runs
session = get_session()

# Fetch and display articles
articles = session.query(Article).order_by(Article.published_at.desc()).all()

for article in articles:
    with st.container():
        st.markdown(f"### {article.title}")
        st.write(article.description)
        st.markdown(f"[🔗 Read More]({article.url})", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Source:** {article.source}")
        with col2:
            st.markdown(f"**Published At:** {article.published_at.strftime('%Y-%m-%d %H:%M')}")

        st.markdown("---")
