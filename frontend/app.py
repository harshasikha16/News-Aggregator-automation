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
st.markdown("""
    <style>
        .header {
            text-align: center;
            margin-block-end: 30px;
        }
        .header h1 {
            font-size: 2.5rem;
            color: #333;
        }
        .header p {
            font-size: 1.2rem;
            color: #666;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .grid-item {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background-color: #f9f9f9;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .grid-item h3 {
            margin: 0 0 10px;
            font-size: 1.2rem;
            color: #333;
        }
        .grid-item p {
            font-size: 0.9rem;
            color: #555;
        }
        .grid-item a {
            color: #007BFF;
            text-decoration: none;
            font-weight: bold;
        }
        .grid-item a:hover {
            text-decoration: underline;
        }
        .grid-item .meta {
            font-size: 0.8rem;
            color: gray;
            margin-block-start: 10px;
            display: flex;
            justify-content: space-between;
        }
    </style>
    <div class="grid-container">
""", unsafe_allow_html=True)

for article in articles:
    st.markdown(f"""
        <div class="grid-item">
            <h3>{article.title}</h3>
            <p>{article.description}</p>
            <a href="{article.url}" target="_blank">🔗 Read More</a>
            <div class="meta">
                <div><b>Source:</b> {article.source}</div>
                <div><b>Published At:</b> {article.published_at.strftime('%Y-%m-%d %H:%M')}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
