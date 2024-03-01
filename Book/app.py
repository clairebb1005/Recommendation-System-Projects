from database import create_session, Book, get_db
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models_pd import recommend_collaborative_filtering_test
from books import BookData


class BookBase(BaseModel):
    isbn: str
    book_title: str
    book_author: str
    year_of_publication: int
    publisher: str
    image_url_s: str
    image_url_m: str
    image_url_l: str


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class RecommendationRequest(BaseModel):
    user_id: int


class RecommendationResponse(BaseModel):
    book_id: str
    estimated_rating: float


# Initialize the session
db_path = 'sqlite:///books.db'
session = create_session(db_path)

# Initialize FastAPI
app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Book Recommendation API!"}


# Show a existed book
@app.get("/books/{isbn}", status_code=status.HTTP_200_OK)
async def get_book(isbn: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.isbn == isbn).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


# API endpoint to add a new book
@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def add_book(book_data: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book_data.dict())
    db.add(new_book)
    db.commit()
    return new_book


# Update a book information
@app.put("/books/{isbn}", status_code=status.HTTP_200_OK)
async def update_book(isbn: str, book_update: BookUpdate, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.isbn == isbn).first()
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in book_update.dict().items():
        setattr(existing_book, field, value)

    db.commit()
    return existing_book


# API endpoint to delete an existing book
@app.delete("/books/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(isbn: str, db: Session = Depends(get_db)):
    existing_book = db.query(Book).filter(Book.isbn == isbn).first()
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(existing_book)
    db.commit()
    return {"message": "Book deleted successfully"}


# Recommend a book based on user's history
@app.post("/recommendations/", response_model=List[RecommendationResponse], status_code=status.HTTP_200_OK)
async def get_recommendations(request: RecommendationRequest):
    user_id = request.user_id
    book_data = BookData(ratings_file="data/Ratings.csv", books_file="data/Books.csv", users_file="data/Users.csv")

    # Get recommendations for the user
    recommendations = recommend_collaborative_filtering_test(book_data, 'knn', user_id, n=10)
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found for the user")

    # Format recommendations for response
    response_recommendations = []
    for book_id, estimated_rating in recommendations:
        response_recommendations.append({"book_id": book_id, "estimated_rating": estimated_rating})

    return response_recommendations
