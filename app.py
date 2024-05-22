import streamlit as st 
import pickle
import pandas as pd
import requests

with open("style.css") as f :
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=c3dd0b25c2b49fc97a1dd8adda4eb058&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


movies_dic = pickle.load(open("movie_dict.pkl","rb"))
movies_list = pd.DataFrame(movies_dic)
similarity = pickle.load(open("similarity.pkl","rb"))
# print(movies_list)

def recommend(movie):
    movie_index = movies_list[movies_list["title"] == movie].index[0]
    distances = similarity[movie_index]
    moviesList = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[0:6]
    recommend_movies = []
    recommend_movies_poster = []
    for i in moviesList:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommend_movies.append(movies_list.iloc[i[0]].title)
        # fetch poster from API
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_poster

print(recommend("Avatar"))



st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
"How would you like to be contacted?",
movies_list["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5, col6 = st.columns(6)

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
    with col6:
        st.text(names[5])
        st.image(posters[5])

st.balloons()
