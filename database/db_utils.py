from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Article
from datetime import datetime

engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)
session = Session()

def add_article(article_data):
    article = Article(
        title=article_data['title'],
        description=article_data['description'],
        url=article_data['url'],
        published_at=datetime.fromisoformat(article_data['publishedAt'].replace('Z', '+00:00')),
        source=article_data['source']
    )
    session.add(article)
    session.commit()

def get_all_articles():
    return session.query(Article).all()
