import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarities = pickle.load(open('angle_distance.pkl', 'rb'))

def get_movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZjcyMGVlYjMwMDgxZWQzZmEwNjJhOGUwMTBlNDY4OSIsInN1YiI6IjY0ODcyMWY4YzAzNDhiMDBjODJmM2M0NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IVjkANHAh-pzszrwf6XIvC5TW8Yoa_knEsBXw4Y8kbI"
    }

    response = requests.get(url, headers=headers)
    movie_details = response.json()
    return 'https://image.tmdb.org/t/p/original' + movie_details['poster_path']

# Pre-built recommendation function
def recommend_movie(movie):
    recommendation_movies = []
    recommendation_posters = []
    movie_index = movies[movies['title'] == movie].index[0]
    # similarity score with other movies row
    distances = similarities[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommendation_movies.append(movies.iloc[i[0]].title)
        recommendation_posters.append(get_movie_poster(movie_id))
    return recommendation_movies, recommendation_posters


def main():
    st.set_page_config(layout="wide")

    st.title("Movie Recommendation System")

    st.write("Select a Movie from the Dropdown List")

    # List of movie names
    movie_list = movies['title'].values

    selected_movie = st.selectbox("Select a movie", movie_list, key="movie", help="")

    if st.button("Get Recommendations", key="recommend"):
        if selected_movie:
            # Call the recommendation function
            recommended_movies, recommended_posters = recommend_movie(selected_movie)

            st.write("Selected Movie:")
            st.write(selected_movie)

            st.write("Top 5 Recommended Movies:")

            # Display the movie titles and posters
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.markdown(f"<p style='font-weight:bold;'>{recommended_movies[0]}</p>", unsafe_allow_html=True)
                st.image(recommended_posters[0])
            with col2:
                st.markdown(f"<p style='font-weight:bold;'>{recommended_movies[1]}</p>", unsafe_allow_html=True)
                st.image(recommended_posters[1])

            with col3:
                st.markdown(f"<p style='font-weight:bold;'>{recommended_movies[2]}</p>", unsafe_allow_html=True)
                st.image(recommended_posters[2])
            with col4:
                st.markdown(f"<p style='font-weight:bold;'>{recommended_movies[3]}</p>", unsafe_allow_html=True)
                st.image(recommended_posters[3])
            with col5:
                st.markdown(f"<p style='font-weight:bold;'>{recommended_movies[4]}</p>", unsafe_allow_html=True)
                st.image(recommended_posters[4])

    # Add your personal information
    st.markdown("---")
    st.write("Developed by [Sarthak Bhatore](https://www.linkedin.com/in/sarthak-bhatore-004aaa1ba/)")

if __name__ == "__main__":
    main()
