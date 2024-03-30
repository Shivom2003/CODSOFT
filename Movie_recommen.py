import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import numpy as np

# Load the data
ratings = pd.read_csv("https://s3-us-west-2.amazonaws.com/recommender-tutorial/ratings.csv")
movies = pd.read_csv("https://s3-us-west-2.amazonaws.com/recommender-tutorial/movies.csv")

# Function to create a user-item matrix
def create_matrix(df):
    N = len(df['userId'].unique())
    M = len(df['movieId'].unique())
    user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
    movie_mapper = dict(zip(np.unique(df["movieId"]), list(range(M))))
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
    movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["movieId"])))
    user_index = [user_mapper[i] for i in df['userId']]
    movie_index = [movie_mapper[i] for i in df['movieId']]
    X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))
    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)

# Function to find similar movies
def find_similar_movies(movie_id, X, k, movie_mapper, movie_inv_mapper, metric='cosine'):
    if movie_id not in movie_mapper:
        return []
    movie_ind = movie_mapper[movie_id]
    kNN = NearestNeighbors(n_neighbors=min(k + 1, X.shape[0]), algorithm="brute", metric=metric)
    kNN.fit(X)
    movie_vec = X[movie_ind].reshape(1, -1)
    distances, indices = kNN.kneighbors(movie_vec, return_distance=True)
    neighbour_ids = []
    for i in range(1, len(indices[0])):
        n = indices[0][i]
        neighbour_ids.append(movie_inv_mapper[n])
    return neighbour_ids

# Improved GUI code
class MovieRecommenderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Movie Recommender System")

        # Improved layout with padding
        self.label = tk.Label(master, text="Enter User ID:", font=("Arial", 14))
        self.label.grid(row=0, column=0, pady=10, padx=10)

        self.user_id_entry = tk.Entry(master, font=("Arial", 14))
        self.user_id_entry.grid(row=0, column=1, pady=10, padx=10)

        self.get_recommendation_button = tk.Button(master, text="Get Recommendations", command=self.recommend_movies, font=("Arial", 14))
        self.get_recommendation_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

        self.recommendation_label = tk.Label(master, text="", font=("Arial", 12))
        self.recommendation_label.grid(row=2, column=0, columnspan=2)

    def recommend_movies(self):
        user_id = int(self.user_id_entry.get())
        df_user = ratings[ratings['userId'] == user_id]
        if df_user.empty:
            messagebox.showinfo("Error", "User ID not found.")
            return
        movie_id = df_user[df_user['rating'] == df_user['rating'].max()]['movieId'].iloc[0]
        similar_ids = find_similar_movies(movie_id, X, 10, movie_mapper, movie_inv_mapper)
        movie_titles = dict(zip(movies['movieId'], movies['title']))
        recommendations = [movie_titles.get(i, "Movie not found") for i in similar_ids]
        
        watched_movie_title = movie_titles.get(movie_id, "Watched movie not found")
        recommendation_text = f"Since you watched {watched_movie_title}, Recommendations:\n\n" + "\n".join(recommendations)
        
        self.recommendation_label.config(text=recommendation_text, justify=tk.LEFT, anchor="w")


def main():
    root = tk.Tk()
    app = MovieRecommenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
