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
        <div style="margin-bottom: 40px;">
            <h3>{article.title}</h3>
            <p>{article.description}</p>
            <a href="{article.url}" target="_blank">🔗 Read More</a>
            <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 12px; color: gray;">
                <div><b>Source:</b> {article.source}</div>
                <div><b>Published At:</b> {article.published_at.strftime('%Y-%m-%d %H:%M')}</div>
            </div>
            <hr style="margin-top: 20px;">
        </div>
    """, unsafe_allow_html=True)
