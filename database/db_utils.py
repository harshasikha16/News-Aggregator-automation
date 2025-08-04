from sqlalchemy.exc import IntegrityError
from database.models import Article
from sqlalchemy.orm import sessionmaker
from database.models import engine

Session = sessionmaker(bind=engine)
session = Session()

def add_article(news_item):
    # Check if article with same URL exists
    existing_article = session.query(Article).filter_by(url=news_item['url']).first()
    if existing_article:
        # Update existing article
        existing_article.title = news_item['title']
        existing_article.description = news_item['description']
        existing_article.published_at = news_item['publishedAt']
        existing_article.source = news_item['source']
    else:
        # Add new article
        article = Article(
            title=news_item['title'],
            description=news_item['description'],
            url=news_item['url'],
            published_at=news_item['publishedAt'],
            source=news_item['source']
        )
        session.add(article)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print(f"Failed to add article: {news_item['title']}")
        