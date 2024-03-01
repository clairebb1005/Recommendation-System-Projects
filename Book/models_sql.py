from sqlalchemy import func
from surprise import Reader, Dataset, KNNBasic
from database import Rating, Book, User
from utils import load_model, save_model


def recommend_popularity_based_sql(session, min_ratings=500, num_recommendations=50):
    # Query to calculate average rating and total ratings for each book
    query = session.query(
        Rating.isbn,
        func.avg(Rating.book_rating).label('average_rating'),
        func.count(Rating.book_rating).label('total_ratings')
    ).group_by(Rating.isbn).subquery()

    # Query to filter books with more than min_ratings and sort them by average rating
    popularity = session.query(
        query.c.isbn,
        query.c.average_rating,
        query.c.total_ratings
    ).filter(query.c.total_ratings > min_ratings).order_by(query.c.average_rating.desc()).limit(
        num_recommendations).all()

    return popularity


def recommend_collaborative_filtering_preprocessing_sql(session):
    # Subquery to get popular books with more than 50 ratings
    popular_books_subquery = session.query(Rating.isbn). \
        join(Book, Book.isbn == Rating.isbn). \
        group_by(Rating.isbn). \
        having(func.count(Rating.isbn) > 50). \
        subquery()

    # Query to filter active users and popular books directly in the database
    filtered_ratings = session.query(Rating). \
        join(User, User.user_id == Rating.user_id). \
        join(popular_books_subquery, Rating.isbn == popular_books_subquery.c.isbn). \
        group_by(Rating.user_id). \
        having(func.count(Rating.user_id) > 200).all()

    active_users = [rating.user_id for rating in filtered_ratings]
    popular_books = [rating.isbn for rating in filtered_ratings]

    return active_users, popular_books, filtered_ratings


def recommend_collaborative_filtering_train_sql(filtered_ratings):
    # Assuming ratings are on a scale of 0 to 10
    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df([(rating.user_id, rating.isbn, rating.book_rating) for rating in filtered_ratings],
                                reader)

    # Train the model on the entire dataset
    model = KNNBasic()
    trainset = data.build_full_trainset()
    model.fit(trainset)

    # Save the trained model
    save_model('knn', model)


def recommend_collaborative_filtering_test_sql(session, model_path, user_id, n=10):
    model = load_model(model_path)

    # Remove books already rated by the user
    rated_books = session.query(Rating.isbn).filter(Rating.user_id == user_id).all()
    rated_books = [isbn for isbn, in rated_books]
    books = session.query(Book.isbn).all()
    books = [book for book in books]
    unrated_books = [book_isbn for book_isbn in books if book_isbn not in rated_books]

    # Make predictions for unrated books
    predictions = [model.predict(user_id, book_isbn) for book_isbn in unrated_books]

    # Sort predictions by estimated rating in descending order
    predictions.sort(key=lambda x: x.est, reverse=True)

    # Get top N recommendations
    top_n_recommendations = [(prediction.iid, prediction.est) for prediction in predictions[:n]]

    return top_n_recommendations
