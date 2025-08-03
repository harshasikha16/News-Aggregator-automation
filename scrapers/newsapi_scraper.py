import requests
import sys
import os
from database.models import Base, engine
from database.db_utils import add_article
from datetime import datetime

# Ensure DB exists
if not os.path.exists('news.db'):
    Base.metadata.create_all(engine)

# Get category argument from CLI (default to general)
category = sys.argv[1] if len(sys.argv) > 1 else "general"

# Build NewsAPI URL dynamically
API_KEY = '84175952cada4755bcd02b4336412205'
URL = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&pageSize=20&apiKey={API_KEY}'

# Fetch News
response = requests.get(URL)
data = response.json()
articles = data.get('articles', [])

# Process & Store Articles
for article in articles:
    if not article.get('title') or not article.get('url'):
        continue  # Skip incomplete data

    news_item = {
        'title': article['title'],
        'description': article.get('description', ''),
        'url': article['url'],
        'publishedAt': article.get('publishedAt', datetime.utcnow().isoformat()),
        'source': article['source']['name']
    }

    add_article(news_item)
    print(f"Processed: {news_item['title']}")
