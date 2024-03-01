import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from books import BookData
from utils import load_model, save_model
import random

def recommend_popularity_based_pd(Books, min_ratings=500, num_recommendations=50):
    # Calculate the average rating for each book
    average_ratings = Books.ratings.groupby('ISBN')['Book-Rating'].mean().reset_index()

    # Calculate the total number of ratings for each book
    total_ratings = Books.ratings.groupby('ISBN')['Book-Rating'].count().reset_index()

    # Merge average_ratings and total_ratings
    popularity = pd.merge(average_ratings, total_ratings, on='ISBN')

    # Rename columns
    popularity.columns = ['ISBN', 'Average-Rating', 'Total-Ratings']

    # Filter books with more than 500 ratings and sort them by average rating
    popularity = popularity[popularity['Total-Ratings'] > min_ratings].sort_values(by=['Average-Rating'],
                                                                                   ascending=False).reset_index(
        drop=True)

    return popularity.head(num_recommendations)


def recommend_collaborative_filtering_preprocessing(book_data):
    # Preprocess the data so that local CPU and RAM are sufficient
    ratings_per_user = book_data.ratings.groupby('User-ID').size()
    popular_books = book_data.ratings.groupby('ISBN').size()

    # Filter users who have rated more than 200 books
    active_users = ratings_per_user[ratings_per_user > 200].index

    # Filter books with at least 50 ratings
    popular_books = popular_books[popular_books > 50].index

    # Filter the ratings dataframe based on active users and popular books
    filtered_ratings = book_data.ratings[(book_data.ratings['User-ID'].isin(active_users)) &
                                         (book_data.ratings['ISBN'].isin(popular_books))]

    return active_users, popular_books, filtered_ratings


def recommend_collaborative_filtering_train(filtered_ratings):

    # Assuming ratings are on a scale of 0 to 10
    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df(filtered_ratings[['User-ID', 'ISBN', 'Book-Rating']], reader)

    # Train the model on the entire dataset
    model = KNNBasic()
    trainset = data.build_full_trainset()
    model.fit(trainset)

    # Save the trained model
    save_model('knn', model)


def recommend_collaborative_filtering_test(book_data, model_path, user_id, n=10):
    model = load_model(model_path)

    # Remove books already rated by the user
    rated_books = list(book_data.ratings[book_data.ratings['User-ID'] == user_id]['ISBN'])
    unrated_books = [book_isbn for book_isbn in book_data.books['ISBN'] if book_isbn not in rated_books]

    # Make predictions for unrated books
    predictions = [model.predict(user_id, book_isbn) for book_isbn in unrated_books]

    # Sort predictions by estimated rating in descending order
    predictions.sort(key=lambda x: x.est, reverse=True)

    # Get top N recommendations
    top_n_recommendations = [(prediction.iid, prediction.est) for prediction in predictions[:n]]

    return top_n_recommendations


if __name__ == '__main__':
    book_data = BookData(ratings_file="data/Ratings.csv", books_file="data/Books.csv", users_file="data/Users.csv")

    # Popularity based
    popular_books = recommend_popularity_based_pd(book_data)
    print(popular_books)

    # Collaborative Filtering: Data Preprocessing, Train, Recommend
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
