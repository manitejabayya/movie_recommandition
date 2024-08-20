import streamlit as st
import pickle
import requests

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None

# Load the movie list and similarity matrix
movies = pickle.load(open("movie_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['original_title'].values

# Streamlit app interface
st.header("Movie Recommendation System")

# Create a dropdown to select a movie
selected_movie = st.selectbox("Select a movie:", movies_list)

# Recommendation function used in the app
def recommend(movie):
    index = movies[movies['original_title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# When the "Recommend" button is clicked, display recommendations
if st.button("Recommend"):
    movie_names, movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, movie_names, movie_posters):
        with col:
            st.text(name)
            if poster:
                st.image(poster)
            else:
                st.text("Poster not available")
