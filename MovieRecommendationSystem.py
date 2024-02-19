import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch a movie poster using the movie_id
def fetch_movie_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=8c123cb589ca533f6089cc45ea32eaa4&language=en-US'.format(
            movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']


# Function to recommend similar movies
def recommend_similar_movies(movie_title):
    movie_index = movie_data[movie_data['title'] == movie_title].index[0]
    distances = similarity_matrix[movie_index]
    movie_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        movie_id = movie_data.iloc[i[0]].movie_id
        # Fetch the movie poster from the API
        recommended_movies.append(movie_data.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_movie_poster(movie_id))
    return recommended_movies, recommended_movie_posters


# Load movie data from the pickled file
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movie_data = pd.DataFrame(movies_dict)

# Load similarity data from the pickled file
similarity_matrix = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title and background image
st.title("Movie Recommendation System")

# User selects a movie from the dropdown
selected_movie_name = st.selectbox(
    'Select a Movie !!',
    movie_data['title'].values)

# Recommendation button
if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend_similar_movies(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
