import os
import json
class DataManager:
    def __init__(self, filename):
        self.filename = filename
        self.movies = self.load_movies()

    def load_movies(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}

    def save_movies(self):
        with open(self.filename, 'w') as file:
            json.dump(self.movies, file)

    def add_movie(self, movie):
        self.movies[movie.movie_id] = movie