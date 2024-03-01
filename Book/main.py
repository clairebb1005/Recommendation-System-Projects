from database import init_db, create_session
from models_sql import recommend_popularity_based_sql
from models_pd import recommend_popularity_based_pd
from books import BookData
import warnings
warnings.filterwarnings('ignore')

# SQL implementation
database_exist = True

if not database_exist:
    init_db()

# Initialize the session
db_path = 'sqlite:///books.db'
session = create_session(db_path)

# Call the recommend_popularity_based function
popularity = recommend_popularity_based_sql(session)

# Print or return the popularity
print(popularity)

# Pandas Dataframe implementation
book_data = BookData(ratings_file="data/Ratings.csv", books_file="data/Books.csv", users_file="data/Users.csv")
popular_books = recommend_popularity_based_pd(book_data)
print(popular_books)
