# Book Recommendation System

`Book` repository hosts a sophisticated book recommendation system employing SQL and pandas-based methods. The system leverages two key strategies: (1) popularity-based recommendations, which rely on average ratings and total ratings of books, and (2) collaborative filtering, which utilizes the KNN algorithm to suggest books to users based on their interactions with similar users.

### Dataset
The dataset used for this project can be downloaded from [Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset?resource=download). After downloading, extract the contents into a directory named `data` inside `Book` repository.

## Models

- **Pandas-based Models**:
  - `recommend_popularity_based_pd`: Recommends popular books based on pandas DataFrame.
  - `recommend_collaborative_filtering_preprocessing`: Preprocesses the data for collaborative filtering.
  - `recommend_collaborative_filtering_train`: Trains the collaborative filtering model.
  - `recommend_collaborative_filtering_test`: Tests the collaborative filtering model by generating recommendations for a given user.

- **SQL-based Models**:
  - `recommend_popularity_based_sql`: Recommends popular books based on SQL database using SQLAlchemy.
  - `recommend_collaborative_filtering_preprocessing_sql`: Preprocesses the data for collaborative filtering using SQL.
  - `recommend_collaborative_filtering_train_sql`: Trains the collaborative filtering model.
  - `recommend_collaborative_filtering_test_sql`: Tests the collaborative filtering model by generating recommendations for a given user using SQL.

## Files

- `books.py`: Contains the `BookData` class to load and store data using pandas.
- `database.py`: Contains SQLAlchemy models and functions to interact with the SQLite database.
- `models_pd.py`: Contains pandas-based recommendation models.
- `models_sql.py`: Contains SQL-based recommendation models.
- `main.py`: Demonstrates how to use both SQL and pandas-based approaches for book recommendation.
- `app.py`: Contains the FastAPI application for CRUD operations on books to manipulate the database and generate recommendations by giving user-id using a trained KNN model.
- `utils.py`: Contains load and save model functions.
- `knn`: The trained KNN model.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Recommendation-System-Projects
   ```
3. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Train the model and see the results:
   ```bash
   python main.py
   ```
5. Access the FastAPI Swagger UI:
Use `uvicorn app:app --reload` command under `Book` repository.
Open your web browser and go to http://127.0.0.1:8000/docs to test the FastAPI application for CRUD operations on books and to generate recommendations using collaborative filtering.
6. Build Dockerfile: 
   ```bash
   docker build -t recommendation-app .
   docker run -d -p 8000:8000 recommendation-app
   ```
   You can access http://localhost:8000/ after built.


## License

This project is licensed under the MIT License.
