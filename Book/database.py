from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pandas as pd

# Define the database URL
SQLALCHEMY_DATABASE_URL = 'sqlite:///./books_test.db'

# Create the SQLAlchemy engine to open up and use database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A database object which is to control our database
Base = declarative_base()


# Define SQLAlchemy models
class Rating(Base):
    __tablename__ = 'ratings'

    index = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    isbn = Column(String)
    book_rating = Column(Integer)


class Book(Base):
    __tablename__ = 'books'

    isbn = Column(String, primary_key=True, index=True)
    book_title = Column(String)
    book_author = Column(String)
    year_of_publication = Column(Integer)
    publisher = Column(String)
    image_url_s = Column(String)
    image_url_m = Column(String)
    image_url_l = Column(String)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    age = Column(Integer)


# Initialize database with data from CSV files
def init_db():
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    # Load data from CSV files and rename them to fit the database column name
    ratings = pd.read_csv('data/Ratings.csv')
    ratings.columns = ['user_id', 'isbn', 'book_rating']

    books = pd.read_csv('data/Books.csv')
    books.columns = ['isbn', 'book_title', 'book_author', 'year_of_publication', 'publisher', 'image_url_s',
                     'image_url_m', 'image_url_l']

    users = pd.read_csv('data/Users.csv')
    users.columns = ['user_id', 'location', 'age']

    # Insert data into database
    ratings.to_sql('ratings', engine, if_exists='append', index=True)
    books.to_sql('books', engine, if_exists='append', index=False)
    users.to_sql('users', engine, if_exists='append', index=False)

    session.commit()
    session.close()


def create_session(db_path):
    # Initialize the database connection
    engine = create_engine(db_path)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    return session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == '__main__':
    # Initialize the database
    init_db()
