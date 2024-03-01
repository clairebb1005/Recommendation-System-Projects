import pandas as pd


class BookData:
    def __init__(self, ratings_file, books_file, users_file):
        self.ratings = pd.read_csv(ratings_file)
        self.books = pd.read_csv(books_file)
        self.users = pd.read_csv(users_file)
        self.book_ratings = pd.merge(self.ratings, self.books, on='ISBN')
        self.book_ratings_users = pd.merge(self.book_ratings, self.users, on='User-ID')
