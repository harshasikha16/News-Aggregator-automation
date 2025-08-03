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

# ---- Title ----
st.title("📰 News Aggregator Dashboard")

# ---- Refresh Button ----
if st.button("🔄 Refresh News"):
    with st.spinner("Fetching latest news..."):
        subprocess.run(["python", "scrapers/newsapi_scraper.py"])
    st.rerun()

# ---- DB Connection ----
engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)
session = Session()

# ---- Fetch Articles from DB ----
articles = session.query(Article).order_by(Article.published_at.desc()).all()

# ---- Display Articles ----
for article in articles:
    st.markdown(f"""
        <div class="news-card">
            <div class="news-title">{article.title}</div>
            <div class="news-description">{article.description}</div>
            <div class="news-meta">{article.source} | {article.published_at.strftime('%Y-%m-%d %H:%M')}</div>
            <a href="{article.url}" target="_blank">Read More</a>
        </div>
    """, unsafe_allow_html=True)

# ---- CSS Styling ----
st.markdown("""
    <style>
        .news-card {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            padding: 15px;
            margin-bottom: 20px;
        }

        .news-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .news-description {
            font-size: 14px;
            margin-bottom: 10px;
        }

        .news-meta {
            font-size: 12px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)
