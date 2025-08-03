import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime
import subprocess

# Add project path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.models import Article

# DB Connection
engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)
session = Session()

# ---- Feedly Style UI Injection ----
st.markdown(""" 
    <style>
        /* Paste entire CSS+HTML from Canvas here */
        /* (Just the <style>...</div> block you have in Canvas) */
    </style>

    <div class="sidebar">
        <h3>Feeds</h3>
        <a href="?category=technology">Technology</a>
        <a href="?category=business">Business</a>
        <a href="?category=sports">Sports</a>
        <a href="?category=science">Science</a>
        <a href="?category=health">Health</a>
        <a href="?category=entertainment">Entertainment</a>
    </div>

    <div class="main-content">
        <div class="custom-container">
    """, unsafe_allow_html=True)

# ---- Handle Category from URL ----
query_params = st.query_params.to_dict()
selected_category = query_params.get("category", "general")

# ---- Refresh Button ----
if st.button("🔄 Refresh News"):
    with st.spinner("Fetching latest news..."):
        subprocess.run(["python", "scrapers/newsapi_scraper.py", selected_category])
    st.rerun()

# ---- Fetch & Display Articles ----
articles = session.query(Article).order_by(Article.published_at.desc()).all()

for article in articles:
    if article.published_at.date() != datetime.today().date():
        continue  # Skip articles not from today

    st.markdown(f"""
        <div class="news-card">
            <img src="{article.urlToImage or 'https://via.placeholder.com/120x80'}" class="news-image" alt="News Thumbnail">
            <div class="news-content">
                <div class="news-title">{article.title}</div>
                <div class="news-meta">{article.source} | {article.published_at.strftime('%Y-%m-%d %H:%M')}</div>
                <a href="{article.url}" class="news-link" target="_blank">Read More</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---- Close main content div ----
st.markdown("</div></div>", unsafe_allow_html=True)
