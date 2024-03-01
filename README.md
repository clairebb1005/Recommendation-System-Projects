# Book Recommendation System

`Book` repository contains an implementation of a book recommendation system using both SQL and pandas-based approaches. The recommendation system is based on popularity, where books are recommended based on their average ratings and total number of ratings.

### Dataset
The dataset used for this project can be downloaded from [Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?resource=download). After downloading, extract the contents into a directory named `data` inside `Book` repository.

## Models

- **Pandas-based Models**:
  - `recommend_popularity_based_pd`: Recommends popular books based on pandas DataFrame.

- **SQL-based Models**:
  - `recommend_popularity_based_sql`: Recommends popular books based on SQL database using SQLAlchemy.

## Files

- `books.py`: Contains the `BookData` class to load and store data using pandas.
- `database.py`: Contains SQLAlchemy models and functions to interact with the SQLite database.
- `models_pd.py`: Contains pandas-based recommendation models.
- `models_sql.py`: Contains SQL-based recommendation models.
- `main.py`: Demonstrates how to use both SQL and pandas-based approaches for book recommendation.
- `app.py`: Contains the FastAPI application for CRUD operations on books to manipulate the database. Use `uvicorn app:app --reload` command under `Book` repository and go to `http://127.0.0.1:8000/docs#` to test it.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```
   
2. Navigate to the project directory:
   ```bash
   cd Recommendation-System-Projects
   ```
4. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## License

This project is licensed under the MIT License.
