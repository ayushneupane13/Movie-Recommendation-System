import streamlit as st
import pickle
import numpy as np
import requests
import gdown
import os

API_KEY = "65db57157158b91b4c92ce83603f3c0d"

# ✅ Google Drive file ID for similarity.pkl
# Link: https://drive.google.com/file/d/10qgak0we__k1ZoypqVIdXTkV8Ef8Y2j0/view?usp=sharing
file_id = "10qgak0we__k1ZoypqVIdXTkV8Ef8Y2j0"
url = f"https://drive.google.com/uc?id={file_id}"

# ✅ Download similarity.pkl if not present
if not os.path.exists("similarity.pkl"):
    with st.spinner("Downloading model file... (this happens only once)"):
        gdown.download(url, "similarity.pkl", quiet=False)

# ✅ Load data
movies = pickle.load(open("movies.pkl", "rb"))

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = np.where(movies["title"].values == movie)[0][0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# ✅ Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])
