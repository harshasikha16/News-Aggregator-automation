from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    url = Column(String, unique=True)
    published_at = Column(DateTime)
    source = Column(String)

# Create SQLite DB (news.db)
engine = create_engine('sqlite:///news.db')
Base.metadata.create_all(engine)
