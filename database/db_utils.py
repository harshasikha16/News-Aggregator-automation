from sqlalchemy.exc import SQLAlchemyError
from database.models import Article, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

def add_article(news_item):
    session = Session()  # Create fresh session per call

    try:
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

        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Failed to add/update article: {news_item['title']}")
        print(f"Error: {e}")
    finally:
        session.close()  # Always close session after operation
