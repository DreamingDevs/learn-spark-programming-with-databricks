## Create a sample dataset

Data is the main prerequisite for developing our spark applications. In this section we will generate a `MovieRatings` dataset with the help of ChatGPT.

> Prompt: I am learning spark and databricks and planning to execute few exercises. I need following sample json files for testing. Users (100,000), Movies (20000), MovieRatings (1,000,000).

Users (100,000 entries):
```
user_id (unique identifier)
name
email
gender
age
join_date
```

Movies (20,000 entries):
```
movie_id (unique identifier)
title
genre
release_year
duration (in minutes)
```

MovieRatings (1,000,000 entries):

```
rating_id (unique identifier)
user_id
movie_id
rating (1 to 5 stars)
rating_date
```

ChatGTP graciously gave me the Python code which after minor modifications by me can be found at [create_dataset.py](./../src/create_dataset.py). `Faker` and `Pandas` are the dependencies, which are abstracted to [requirements.txt](./../src/requirements.txt). Execute the code as shown below in the terminal.

> NOTE: Make sure Python virtual env. is active.

```
cd learn-spark-programming-with-databricks
cd src
pip install -r requirements.txt
python3 create_dataset.py ../dataset
```

Three json files - `movies.json`, `ratings.json` and `users.json` are created at `dataset` folder in the root directory.