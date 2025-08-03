import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime
import subprocess

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.models import Article

# ---- Feedly Style CSS & Sidebar ----
st.markdown(""" 
    <style>
        .custom-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            padding: 10px;
            background-color: #f8f9fa;
        }

        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            width: 220px;
            background: #ffffff;
            border-right: 1px solid #ddd;
            padding: 20px;
        }

        .sidebar h3 {
            font-size: 16px;
            margin-bottom: 10px;
        }

        .sidebar a {
            display: block;
            margin: 5px 0;
            color: #333;
            text-decoration: none;
            font-size: 14px;
        }

        .sidebar a:hover {
            color: #1a73e8;
        }

        .main-content {
            margin-left: 240px;
            padding: 20px;
        }

        .news-card {
            display: flex;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            padding: 15px;
            align-items: center;
        }

        .news-image {
            width: 120px;
            height: 80px;
            background-color: #e0e0e0;
            border-radius: 8px;
            margin-right: 15px;
            object-fit: cover;
        }

        .news-content {
            display: flex;
            flex-direction: column;
        }

        .news-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .news-meta {
            font-size: 12px;
            color: gray;
        }

        .news-link {
            font-size: 14px;
            color: #1a73e8;
            text-decoration: none;
        }
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

# ---- Capture Category Param from URL ----
query_params = st.query_params.to_dict()
selected_category = query_params.get("category", "general")

# ---- Auto-fetch if category changes ----
if "last_category" not in st.session_state or st.session_state.last_category != selected_category:
    with st.spinner(f"Fetching {selected_category} news..."):
        subprocess.run(["python", "scrapers/newsapi_scraper.py", selected_category])
    st.session_state.last_category = selected_category
    st.rerun()

# ---- DB Connection ----
engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)
session = Session()

# ---- Fetch Articles from DB ----
articles = session.query(Article).order_by(Article.published_at.desc()).all()

# ---- Display Articles Dynamically ----
for article in articles:
    if article.published_at.date() != datetime.today().date():
        continue  # Skip non-today articles

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

# ---- Close Main Content Div ----
st.markdown("</div></div>", unsafe_allow_html=True)
