import pandas as pd
import numpy as np

books = pd.read_csv('data/Books.csv')
ratings = pd.read_csv('data/Ratings.csv')
users = pd.read_csv('data/Users.csv')

# ISBN,Book-Title,Book-Author,Year-Of-Publication,Publisher,Image-URL-S,Image-URL-M,Image-URL-L
print("====================================Books===================================")
print(books.head())

# User-ID,ISBN,Book-Rating
print("====================================Ratings===================================")
print(ratings.head())

# User-ID,Location,Age
print("====================================Users===================================")
print(users.head())

book_ratings = books.merge(ratings, on='ISBN')
user_rating = users.merge(ratings, on='User-ID')

print("====================================Book Ratings===================================")
print(book_ratings.head())
print("====================================User Ratings===================================")
print(user_rating.head())

