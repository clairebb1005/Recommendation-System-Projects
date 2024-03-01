from database import Rating
from sqlalchemy import func


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
