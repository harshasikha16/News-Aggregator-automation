import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from database.models import Base, engine, Article
from database.db_utils import add_article
from sqlalchemy.orm import sessionmaker

# Ensure tables exist
Base.metadata.create_all(engine)

# Clear existing articles (TRUNCATE TABLE)
Session = sessionmaker(bind=engine)
session = Session()
session.query(Article).delete()
session.commit()
print("Cleared existing articles from DB")

# NewsAPI Config
API_KEY = '84175952cada4755bcd02b4336412205'  # <-- Your API key
URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

# Fetch News from API
response = requests.get(URL)
data = response.json()
articles = data.get('articles', [])

# Process & Store Articles
for article in articles:
    if not article.get('title') or not article.get('url'):
        continue  # Skip incomplete articles

    # Convert publishedAt to Python datetime object
    published_at_str = article.get('publishedAt', '')
    published_at = None
    if published_at_str:
        try:
            published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            published_at = datetime.utcnow()  # Fallback in case format fails

    news_item = {
        'title': article['title'],
        'description': article.get('description', ''),
        'url': article['url'],
        'publishedAt': published_at,
        'source': article['source']['name']
    }

    add_article(news_item)
    print(f"Processed: {news_item['title']}")

session.close()  # Close the session properly
