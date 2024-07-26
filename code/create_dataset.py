import json
import random
import os
from faker import Faker
import pandas as pd

fake = Faker()

# Parameters
num_users = 100000
num_movies = 20000
num_ratings = 1000000

# Generate Users
users = []
for user_id in range(1, num_users + 1):
    user = {
        "user_id": user_id,
        "name": fake.name(),
        "email": fake.email(),
        "gender": random.choice(["Male", "Female", "Other"]),
        "age": random.randint(18, 80),
        "join_date": fake.date_between(start_date='-5y', end_date='today').isoformat()
    }
    users.append(user)

# Generate Movies
movies = []
for movie_id in range(1, num_movies + 1):
    movie = {
        "movie_id": movie_id,
        "title": fake.sentence(nb_words=3, variable_nb_words=True),
        "genre": random.choice(["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi"]),
        "release_year": random.randint(1980, 2024),
        "duration": random.randint(80, 180)
    }
    movies.append(movie)

# Generate MovieRatings
ratings = []
for rating_id in range(1, num_ratings + 1):
    rating = {
        "rating_id": rating_id,
        "user_id": random.randint(1, num_users),
        "movie_id": random.randint(1, num_movies),
        "rating": random.randint(1, 5),
        "rating_date": fake.date_between(start_date='-5y', end_date='today').isoformat()
    }
    ratings.append(rating)

# Save to JSON files
users_df = pd.DataFrame(users)
movies_df = pd.DataFrame(movies)
ratings_df = pd.DataFrame(ratings)

if not os.path.exists('../dataset'):
    os.mkdir('../dataset')

users_df.to_json('../dataset/users.json', orient='records', lines=True)
movies_df.to_json('../dataset/movies.json', orient='records', lines=True)
ratings_df.to_json('../dataset/ratings.json', orient='records', lines=True)

