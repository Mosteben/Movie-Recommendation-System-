class GenreManager:
    def __init__(self):
        self.genres = ["Sport", "Art", "Economic", "Comedy", "Fiction", "Politics"]

    def get_genre_by_index(self, index):
        if 0 <= index < len(self.genres):
            return self.genres[index]
        return None