from database import init_db, create_session
from models_sql import recommend_popularity_based_sql, recommend_collaborative_filtering_preprocessing_sql,\
    recommend_collaborative_filtering_train_sql, recommend_collaborative_filtering_test_sql
from models_pd import recommend_popularity_based_pd, recommend_collaborative_filtering_preprocessing,\
    recommend_collaborative_filtering_train, recommend_collaborative_filtering_test
from books import BookData
from utils import load_model
import warnings
import random
warnings.filterwarnings('ignore')

# SQL implementation
database_exist = True

if not database_exist:
    init_db()

db_path = 'sqlite:///books.db'
session = create_session(db_path)

# Popularity-Based
popularity = recommend_popularity_based_sql(session)
print(popularity)

# Collaborative Filtering
active_users, popular_books, filtered_ratings = recommend_collaborative_filtering_preprocessing_sql(session)
try:
    # Load the model if it exists
    model = load_model('knn')
    print("Trained model loaded.")
except FileNotFoundError:
    recommend_collaborative_filtering_train_sql(filtered_ratings)
random_user_id = random.choice(active_users)
recommendations = recommend_collaborative_filtering_test_sql(session, 'knn', random_user_id, n=10)
print(recommendations)

# Pandas Dataframe implementation
book_data = BookData(ratings_file="data/Ratings.csv", books_file="data/Books.csv", users_file="data/Users.csv")

# Popularity-Based
popular_books = recommend_popularity_based_pd(book_data)
print(popular_books)

# Collaborative Filtering
active_users, popular_books, filtered_ratings = recommend_collaborative_filtering_preprocessing(book_data)
try:
    # Load the model if it exists
    model = load_model('knn')
    print("Trained model loaded.")
except FileNotFoundError:
    recommend_collaborative_filtering_train(filtered_ratings)
random_user_id = random.choice(active_users)
recommendations = recommend_collaborative_filtering_test(book_data, 'knn', random_user_id, n=10)
print(recommendations)