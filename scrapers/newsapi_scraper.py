import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from database.models import Base, engine, Article
from database.db_utils import add_article
from sqlalchemy.orm import sessionmaker

# Ensure DB exists
if not os.path.exists('news.db'):
    Base.metadata.create_all(engine)

# Clear existing articles
Session = sessionmaker(bind=engine)
session = Session()
session.query(Article).delete()
session.commit()
print("Cleared existing articles from DB")

# NewsAPI Config
API_KEY = ''  # <-- Replace with your actual API key
URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

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
        'publishedAt': article.get('publishedAt', ''),
        'source': article['source']['name']
    }

    add_article(news_item)
    print(f"Processed: {news_item['title']}")
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from database.models import Base, engine, Article
from database.db_utils import add_article
from sqlalchemy.orm import sessionmaker

# Ensure DB exists
if not os.path.exists('news.db'):
    Base.metadata.create_all(engine)

# Clear existing articles
Session = sessionmaker(bind=engine)
session = Session()
session.query(Article).delete()
session.commit()
print("Cleared existing articles from DB")

# NewsAPI Config
API_KEY = '84175952cada4755bcd02b4336412205'  # <-- Replace with your actual API key
URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

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
        'publishedAt': article.get('publishedAt', ''),
        'source': article['source']['name']
    }

    add_article(news_item)
    print(f"Processed: {news_item['title']}")
