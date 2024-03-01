import pandas as pd


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
                                                                                ascending=False).reset_index(drop=True)

    return popularity.head(num_recommendations)


if __name__ == '__main__':
    from books import BookData

    book_data = BookData(ratings_file="data/Ratings.csv", books_file="data/Books.csv", users_file="data/Users.csv")
    popular_books = recommend_popularity_based_pd(book_data)
    print(popular_books)
