import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class MovieRecommendationSystemApp:
    def __init__(self, root, data_manager, genre_manager):
        self.root = root
        self.root.title( "Movies Recommendation System" )
        self.data_manager = data_manager
        self.genre_manager = genre_manager
        self.setup_gui()

    def setup_gui(self):
        # Set the overall theme to a dark theme if available or configure a custom one
        self.root.style = ttk.Style()
        self.root.style.theme_use(
            'alt' )  # 'alt', 'default', 'classic', 'clam' are typical options, choose one suitable for your system
        self.root.style.configure( 'TFrame', background='#333333' )
        self.root.style.configure( 'TButton', font=('Helvetica', 12), background='#555555', foreground='white',
                                   borderwidth=1 )
        self.root.style.configure( 'TLabel', font=('Helvetica', 14), background='#333333', foreground='white' )
        self.root.style.map( 'TButton', foreground=[('pressed', 'orange'), ('active', 'white')],
                             background=[('pressed', '!disabled', 'black'), ('active', 'gray')] )

        # Create a frame for the main content with a dark background
        main_frame = ttk.Frame( self.root, padding="30" )
        main_frame.pack( expand=True, fill='both' )

        # Create a label for the title with enhanced styling
        title_label = ttk.Label( main_frame, text="Movie Recommendation System", font=("Arial", 16, 'bold') )
        title_label.pack( pady=10 )

        # Create a frame for the buttons with a dark background
        buttons_frame = ttk.Frame( main_frame )
        buttons_frame.pack( pady=20 )

        # Create buttons with the defined dark style
        buttons_info = [
            ("Add New Movie", self.add_movie),
            ("Update Movie Information", self.update_movie),
            ("Display All Movies", self.display_information_all_movies),
            ("Display Specific Information", self.display_specific_information),
            ("Save Genre in New Files", self.save_by_genre),
            ("Exit", self.exit_program)
        ]

        for text, command in buttons_info:
            button = ttk.Button( buttons_frame, text=text, command=command )
            button.pack( fill="x", pady=10, padx=30, ipady=10, ipadx=10 )

        # Create a separator with a dark color
        ttk.Separator( main_frame, orient="horizontal" ).pack( fill="x", pady=20 )
        # Create a text widget to display information
        self.text_widget = tk.Text( main_frame, height=20, width=80, wrap=tk.WORD )
        self.text_widget.pack( pady=10 )

    def add_movie(self):
        name = simpledialog.askstring( "Movie Name", "Enter the movie name:" )
        if not name:
            messagebox.showerror( "Error", "Movie name cannot be empty!" )
            return
        writer = simpledialog.askstring( "Movie Writer", "Enter the movie writer:" )
        rating = float( simpledialog.askstring( "User Rating", "Enter user rating (1.0 to 5.0):" ) )
        reviews = int( simpledialog.askstring( "Number of Reviews", "Enter the number of reviews:" ) )
        revenue = simpledialog.askstring( "Revenue", "Enter the revenue (e.g., 100.0M):" )
        year = int( simpledialog.askstring( "Year", "Enter the year:" ) )
        genre_number = int( simpledialog.askinteger( "Genre Count", "How many genres (up to 5)?" ) )
        if genre_number > 5:
            messagebox.showerror( "Error", "Cannot enter more than 5 genres." )
            return

        genres = []
        for _ in range( min( genre_number, 5 ) ):
            genre_index = simpledialog.askinteger( "Genre",
                                                   "Enter genre index (0-Sport, 1-Art, 2-Economic, 3-Comedy, 4-Fiction, 5-Politics):" )
            if genre_index is not None and 0 <= genre_index < len( self.genre_manager.genres ):
                genres.append( self.genre_manager.genres[genre_index] )

        base_id = len( self.data_manager.movies ) + 1
        movie_id = f"{base_id}{year}"

        if any( m for m in self.data_manager.movies.values() if
                m['MovieName'].lower() == name.lower() and m['Year'] == year ):
            messagebox.showerror( "Error", "Movie with the same name and year already exists." )
            return

        new_movie = {
            "MovieID": movie_id,
            "MovieName": name,
            "MovieAuthor": writer,
            "UserRating": rating,
            "NumOfReviews": reviews,
            "Revenue": revenue,
            "Year": year,
            "Genre": genres
        }
        self.data_manager.movies[movie_id] = new_movie
        self.data_manager.save_movies()
        messagebox.showinfo( "Success", "Movie added successfully!" )

    def update_movie(self):
        name = simpledialog.askstring( "Movie Name", "Enter the movie name:" )
        if not name:
            messagebox.showerror( "Error", "Movie name cannot be empty!" )
            return
        year = int( simpledialog.askstring( "Year", "Enter the year:" ) )
        movie_to_update = None
        for movie in self.data_manager.movies.values():
            if movie['MovieName'] == name and movie['Year'] == year:
                movie_to_update = movie
        if movie_to_update is None:
            messagebox.showerror( "Error", "Movie Not Found!" )
            return

        movie_id = movie_to_update['MovieID']
        writer = movie_to_update['MovieAuthor']
        rating = movie_to_update['UserRating']
        revenue = movie_to_update['Revenue']
        reviews = movie_to_update['NumOfReviews']
        genres = movie_to_update['Genre']

        answer = messagebox.askyesno( "Acknowledgment", "Update Writer?" )
        if answer:
            writer = simpledialog.askstring( "Movie Writer", "Enter the movie writer:" )

        answer = messagebox.askyesno( "Acknowledgment", "Update Rating?" )
        if answer:
            rating = float( simpledialog.askstring( "User Rating", "Enter user rating (1.0 to 5.0):" ) )

        answer = messagebox.askyesno( "Acknowledgment", "Update Number of reviews?" )
        if answer:
            reviews = int( simpledialog.askstring( "Number of Reviews", "Enter the number of reviews:" ) )

        answer = messagebox.askyesno( "Acknowledgment", "Update Revenue?" )
        if answer:
            revenue = simpledialog.askstring( "Revenue", "Enter the revenue (e.g., 100.0M):" )

        answer = messagebox.askyesno( "Acknowledgment", "Update Genre?" )
        if answer:
            genre_number = int( simpledialog.askinteger( "Genre Count", "How many genres (up to 5)?" ) )
            if genre_number > 5:
                messagebox.showerror( "Error", "Cannot enter more than 5 genres." )
                return
            genres = []
            for _ in range( min( genre_number, 5 ) ):
                genre_index = simpledialog.askinteger( "Genre",
                                                       "Enter genre index (0-Sport, 1-Art, 2-Economic, 3-Comedy, 4-Fiction, 5-Politics):" )
                if genre_index is not None and 0 <= genre_index < len( self.genre_manager.genres ):
                    genres.append( self.genre_manager.genres[genre_index] )

        new_movie = {
            "MovieID": movie_id,
            "MovieName": name,
            "MovieAuthor": writer,
            "UserRating": rating,
            "NumOfReviews": reviews,
            "Revenue": revenue,
            "Year": year,
            "Genre": genres
        }
        self.data_manager.movies[movie_id] = new_movie
        self.data_manager.save_movies()
        messagebox.showinfo( "Success", "Movie updated successfully!" )

    def display_information_all_movies(self):
        choice = int( simpledialog.askstring( "Choice",
                                              "1. Movies sorted by ID\n2. Movies sorted by Name\n3. Movies sorted by Year" ) )
        if choice == 1:
            movies_sorted = self.sort_by_id()
            self.display_sorted_movies( "Sorted by ID", movies_sorted )
        elif choice == 2:
            movies_sorted = self.sort_by_name()
            self.display_sorted_movies( "Sorted by Name", movies_sorted )
        elif choice == 3:
            movies_sorted = self.sort_by_year()
            self.display_sorted_movies( "Sorted by Year", movies_sorted )

    def display_sorted_movies(self, title, movies_sorted):
        # Clear any previous text in the text widget
        self.text_widget.delete( "1.0", tk.END )
        # Display the title
        self.text_widget.insert( tk.END, f"{title}\n\n" )
        # Display the sorted movies
        for movie in movies_sorted:
            self.text_widget.insert( tk.END, f"{movie}\n" )

    def sort_by_id(self):
        pairs = sorted( [(movie['MovieID'], movie['MovieName']) for movie in self.data_manager.movies.values()],
                        key=lambda x: x[0] )
        return [f"{ID}: {name}" for ID, name in pairs]

    def sort_by_name(self):
        pairs = sorted( [movie['MovieName'] for movie in self.data_manager.movies.values()] )
        return [f"{i}: {name}" for i, name in enumerate( pairs )]

    def sort_by_year(self):
        pairs = sorted( [(movie['Year'], movie['MovieName']) for movie in self.data_manager.movies.values()],
                        key=lambda x: x[0] )
        return [f"{year}: {name}" for year, name in pairs]

    def Revenue_Per_Year(self):
        years = list( set( [movie['Year'] for movie in self.data_manager.movies.values()] ) )
        revenue_per_year = {year: 0 for year in years}
        for movie in self.data_manager.movies.values():
            revenue = movie['Revenue']
            if revenue.endswith( 'M' ):
                revenue_numeric = float( revenue[:-1] ) * 1e6
            else:
                revenue_numeric = float( revenue )
            revenue_per_year[movie['Year']] += revenue_numeric
        return [f'year : {year}: ' + 'rev: ' + str( revenue_per_year[year] ) + '\n' for year in
                revenue_per_year.keys()]

    def Average_revenue_Per_Year(self):
        years = list( set( [movie['Year'] for movie in self.data_manager.movies.values()] ) )
        revenue_per_year = {year: 0 for year in years}
        count_per_year = {year: 0 for year in years}
        for movie in self.data_manager.movies.values():
            revenue = movie['Revenue']
            if revenue.endswith( 'M' ):
                revenue_numeric = float( revenue[:-1] ) * 1e6
            else:
                revenue_numeric = float( revenue )
            revenue_per_year[movie['Year']] += revenue_numeric
            count_per_year[movie['Year']] += 1
        return [f'year : {year}: ' + 'avg_rev: ' + str( revenue_per_year[year] / count_per_year[year] ) + '\n' for year
                in
                revenue_per_year.keys()]

    def Movies_per_Author(self):
        writers = list( set( [movie['MovieAuthor'] for movie in self.data_manager.movies.values()] ) )
        movies_per_author = {author: [] for author in writers}
        for movie in self.data_manager.movies.values():
            movies_per_author[movie['MovieAuthor']].append( movie['MovieName'] )
        return [f'author : {writer}: ' + 'movies: ' + str( movies_per_author[writer] ) + '\n' for writer in
                list( movies_per_author.keys() )]

    def Average_revenue_Per_author(self):
        def parse_revenue(revenue_string):
            if revenue_string.endswith( 'M' ):
                # Remove the last character ('M') and convert to float
                number = float( revenue_string[:-1] )
                return number * 1_000_000  # Convert million to actual number
            # Add more conditions if there are other suffixes or formats
            return float( revenue_string )  # Fallback if no suffix
        writers = list( set( [movie['MovieAuthor'] for movie in self.data_manager.movies.values()] ) )
        revenue_per_author = {author: 0 for author in writers}
        counter = {author: 0 for author in writers}
        for movie in self.data_manager.movies.values():
            revenue = parse_revenue( movie['Revenue'] )
            revenue_per_author[movie['MovieAuthor']] += revenue
            counter[movie['MovieAuthor']] += 1

        # To get the average revenue per author, we'll divide the total by the count
        average_revenue_per_author = {
            author: (revenue_per_author[author] / counter[author] )
            for author in writers}

        return average_revenue_per_author

    def display_specific_information(self):
        choice = int( simpledialog.askstring( "Choice",
                                              "1. Revenue Per Year\n2. Average Revenue Per Year\n3. Movies per Author\n4. Average Revenue Per Author" ) )
        if choice == 1:
            revenue_per_year = self.Revenue_Per_Year()
            self.display_information( "Revenue Per Year", revenue_per_year )
        elif choice == 2:
            average_revenue_per_year = self.Average_revenue_Per_Year()
            self.display_information( "Average Revenue Per Year", average_revenue_per_year )
        elif choice == 3:
            movies_per_author = self.Movies_per_Author()
            self.display_information( "Movies per Author", movies_per_author )
        elif choice == 4:
            average_revenue_per_author = self.Average_revenue_Per_author()
            self.display_information( "Average Revenue Per Author", average_revenue_per_author )
        else:
            messagebox.showerror( "Error", "Cannot get more than 4 info." )
            return

    def display_information(self, title, information):
        # Clear any previous text in the text widget
        self.text_widget.delete( "1.0", tk.END )
        # Display the title
        self.text_widget.insert( tk.END, f"{title}\n\n" )
        # Display the information
        for item in information:
            self.text_widget.insert( tk.END, f"{item}\n" )

    def exit_program(self):
        self.root.quit()

    def save_by_genre(self):
        genre_index = simpledialog.askinteger( "Genre Index",
                                               "Enter genre index (0-Sport, 1-Art, 2-Economic, 3-Comedy, 4-Fiction, 5-Politics):" )
        if genre_index is not None and 0 <= genre_index < len( self.genre_manager.genres ):
            genre = self.genre_manager.genres[genre_index]
            movies_of_genre = [movie for movie in self.data_manager.movies.values() if genre in movie['Genre']]
            if not movies_of_genre:
                messagebox.showinfo( "Info", "No movies found for this genre." )
                return

            filename = f"{genre}_movies.txt"
            with open( filename, 'w' ) as file:
                for movie in movies_of_genre:
                    file.write( f"Movie Name: {movie['MovieName']}\n" )
                    file.write( f"Movie Author: {movie['MovieAuthor']}\n" )
                    file.write( f"User Rating: {movie['UserRating']}\n" )
                    file.write( f"Number of Reviews: {movie['NumOfReviews']}\n" )
                    file.write( f"Revenue: {movie['Revenue']}\n" )
                    file.write( f"Year: {movie['Year']}\n" )
                    file.write( f"Genres: {', '.join( movie['Genre'] )}\n\n" )

            messagebox.showinfo( "Success", f"Movies of genre '{genre}' saved in '{filename}' file." )
        else:
            messagebox.showerror( "Error", "Invalid genre index." )
