import requests
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_utils import add_article

API_KEY = '84175952cada4755bcd02b4336412205'
URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

def fetch_news():
    response = requests.get(URL)
    data = response.json()
    articles = data.get('articles', [])
    
    for article in articles:
        news_item = {
            'title': article['title'],
            'description': article['description'],
            'url': article['url'],
            'publishedAt': article['publishedAt'],
            'source': article['source']['name']
        }
        add_article(news_item)
        print(f"Added: {news_item['title']}")

if __name__ == "__main__":
    fetch_news()
