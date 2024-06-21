import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=9bf4a92b91c9dc8c33e3ada9ae13e392')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w185/" + data['poster_path']
    else:
        return "https://via.placeholder.com/185x278.png?text=No+Image"
# Load the movies DataFrame and similarity matrix


movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Extract the titles for the dropdown
movies = movies_df['title'].values


def recommend(movie):
    # Find the movie index in the DataFrame
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Get the top 5 similar movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies_df.iloc[i[0]].title)
    return recommended_movies,recommended_movies_poster


# Streamlit app
st.title('Movie Recommender System')
selected_movie_name = st.selectbox("Select your favourite movie", movies)
if st.button("Recommend similar movies"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

