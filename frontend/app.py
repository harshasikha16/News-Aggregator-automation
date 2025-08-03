import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
import subprocess

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.models import Article

# Setup DB connection
engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)
session = Session()

st.title("📰 News Aggregator Dashboard")

# Refresh Button
if st.button("🔄 Refresh News"):
    with st.spinner("Fetching latest news..."):
        subprocess.run(["python", "scrapers/newsapi_scraper.py"])
    st.success("News updated!")

# Fetch and display articles
articles = session.query(Article).order_by(Article.published_at.desc()).all()

for article in articles:
    st.subheader(article.title)
    st.write(article.description)
    st.markdown(f"[Read More]({article.url})", unsafe_allow_html=True)
    st.write(f"Source: {article.source} | Published At: {article.published_at}")
    st.write("---")
