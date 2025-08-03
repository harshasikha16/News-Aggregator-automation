from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Article
from datetime import datetime

engine = create_engine('sqlite:///news.db')
Session = sessionmaker(bind=engine)
session = Session()

def add_article(article_data):
    existing_article = session.query(Article).filter_by(url=article_data['url']).first()
    if existing_article:
        print(f"Skipped duplicate: {article_data['title']}")
        return

    article = Article(
        title=article_data['title'],
        description=article_data['description'],
        url=article_data['url'],
        published_at=datetime.fromisoformat(article_data['publishedAt'].replace('Z', '+00:00')),
        source=article_data['source']
    )
    session.add(article)
    session.commit()
    print(f"Added: {article_data['title']}")
