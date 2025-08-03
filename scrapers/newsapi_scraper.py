import requests
import sys
import os
from datetime import datetime

# Fix: Ensure Python can locate the 'database' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.models import Base, engine
from database.db_utils import add_article

# Ensure DB exists
if not os.path.exists('news.db'):
    Base.metadata.create_all(engine)

# Get category argument from CLI (default to general)
category = sys.argv[1] if len(sys.argv) > 1 else "general"

# NewsAPI Config
API_KEY = '84175952cada4755bcd02b4336412205'  # <-- Replace this with your actual API key
URL = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=20&apiKey={API_KEY}'

# Fetch News from API
response = requests.get(URL)
data = response.json()
articles = data.get('articles', [])

# Process & Store Articles
for article in articles:
    if not article.get('title') or not article.get('url'):
        continue  # Skip incomplete articles

    news_item = {
        'title': article['title'],
        'description': article.get('description', ''),
        'url': article['url'],
        'publishedAt': article.get('publishedAt', datetime.utcnow().isoformat()),
        'source': article['source']['name']
    }

    add_article(news_item)
    print(f"Processed: {news_item['title']}")
