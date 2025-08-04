import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime
import subprocess

# Add parent directory to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.models import Article

# ---- Title ----
st.title("📰 News Aggregator Dashboard")

# ---- Refresh Button ----
if st.button("🔄 Refresh News"):
    with st.spinner("Fetching latest news..."):
        result = subprocess.run(["python", "scrapers/newsapi_scraper.py"], capture_output=True, text=True)
        st.write(result.stdout)  # Optional: Show logs
    st.rerun()  # Refresh the app after scraping completes

# ---- DB Connection ----
engine = create_engine('sqlite:///news.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# ---- Fetch Articles from DB ----
articles = session.query(Article).order_by(Article.published_at.desc()).all()

# ---- Display Articles in Grid Layout ----
if articles:
    st.markdown("""
        <style>
            .news-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
                gap: 20px;
            }
            .news-card {
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 15px;
                background-color: #fff;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }
            .news-title {
                font-size: 1.2rem;
                font-weight: bold;
                color: #333;
                margin-block-end: 10px;
            }
            .news-description {
                font-size: 0.95rem;
                color: #555;
                margin-block-end: 10px;
            }
            .news-meta {
                font-size: 0.8rem;
                color: gray;
                display: flex;
                justify-content: space-between;
            }
            .read-more {
                font-weight: bold;
                color: #007BFF;
                text-decoration: none;
            }
            .read-more:hover {
                text-decoration: underline;
            }
        </style>
        <div class="news-grid">
    """, unsafe_allow_html=True)

    for article in articles:
        st.markdown(f"""
            <div class="news-card">
                <div class="news-title">{article.title}</div>
                <div class="news-description">{article.description}</div>
                <div class="news-meta">
                    <span><b>Source:</b> {article.source}</span>
                    <span><b>{article.published_at.strftime('%Y-%m-%d %H:%M')}</b></span>
                </div>
                <div style="margin-block-start: 10px;">
                    <a class="read-more" href="{article.url}" target="_blank">🔗 Read More</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No articles found. Try refreshing to fetch latest news.")

# Close session after query
session.close()
