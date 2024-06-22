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
    return recommended_movies, recommended_movies_poster

# Streamlit app
st.title('🎬 Movie Recommender System')
st.markdown("### Find movies similar to your favorites!")

selected_movie_name = st.selectbox("Select your favourite movie", movies)

if st.button("Recommend similar movies"):
    names, posters = recommend(selected_movie_name)
    
    # Display the recommended movies in a nicer layout
    for i in range(5):
        col = st.columns(1)[0]
        with col:
            st.image(posters[i])
            st.write(f"**{names[i]}**")
st.markdown(
    """
    <style>
    .stText {
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
    }
    .stImage {
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
