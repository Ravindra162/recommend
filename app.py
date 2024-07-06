from flask import Flask, render_template, request
import pickle
import requests
import os

app = Flask(__name__)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

@app.route('/')
def index():
    movies = pickle.load(open(os.path.join('artifacts', 'movie_list.pkl'), 'rb'))
    movie_list = movies['title'].values
    return render_template('index.html', movie_list=movie_list)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    selected_movie = request.form['selected_movie']
    movies = pickle.load(open(os.path.join('artifacts', 'movie_list.pkl'), 'rb'))
    similarity = pickle.load(open(os.path.join('artifacts', 'similarity.pkl'), 'rb'))
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
    return render_template('recommendations.html', movie_names=recommended_movie_names, movie_posters=recommended_movie_posters, zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
