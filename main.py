from DataManager import DataManager
import tkinter as tk
from GenreManager import GenreManager
from MovieRecommendationSystemApp import MovieRecommendationSystemApp

if __name__ == "__main__":
    filename = "E:\\project\\movies.txt"
    data_manager = DataManager(filename)
    genre_manager = GenreManager()
    root = tk.Tk()
    app = MovieRecommendationSystemApp(root, data_manager, genre_manager)
    root.mainloop()