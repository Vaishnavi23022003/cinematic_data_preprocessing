# write all of this in home of views.py

from .models import Movie
from .models import Rating
import pandas as pd
import json
import requests
# --------------------------------to save movie recommendations -------------------

file = open('static/json_files/movies_data.json', "r")
data = json.load(file)
file.close()

for i in data:
    s = "|"
    s = s.join([str(k) for k in data[i]['recommendations']])
    m=Movie(id=int(i),
            title=str(data[i]['title']),
            ratings_val=float(data[i]['ratings_val']),
            ratings_total=float(data[i]['ratings_total']),
            recommendations=s)
    m.save()
    break
    print(i, data[i]['title'], data[i]['ratings_val'], data[i]['ratings_total'], data[i]['recommendations'])


# --------------------------to save ratings in Ratings collection------------------------
# reading ratings file:
ratings = pd.read_csv('static/json_files/ratings.csv')

for item,row in ratings.iterrows():
    r=Rating(user_name=str(row['userId']),
             movie_id=int(row['movieId']),
             rating=float(row['rating']))
    r.save()

# ------------------------------- to insert data in Movie collection-------------------

def get_movie_data():
    link = pd.read_csv('static/json_files/links.csv')
    count = 0
    for item, row in link.iterrows():
        movie_id = row['movieId']
        link_id = row['tmdbId']
        t = Movie.objects.get(movie_id=movie_id)
        if t.youtube_id is not None and t.release_date is not None:
            continue
        print(item)

        try:
            response = requests.get(f"https://api.themoviedb.org/3/movie/{link_id}?api_key="
                                    f"006b3879a699dc77c348be4a97c203d9&language=en-US")
            data = response.json()
            poster = data['poster_path']
            title = data['title']
            backdrop = data['backdrop_path']
            release_date = data['release_date']
            overview = data['overview']
            genre = ""
            for i in data['genres']:
                genre += i['name'] + '|'

            t = Movie.objects.get(movie_id=movie_id)
            t.backdrop = backdrop
            t.release_date = release_date
            t.overview = overview
            t.poster = poster
            t.title = title
            t.genre = genre
            t.save()
            print(title)
            response = requests.get(f"https://api.themoviedb.org/3/movie/{link_id}/videos?api_key="
                                    f"006b3879a699dc77c348be4a97c203d9&language=en-US")
            data = response.json()['results']
            youtube_id = data[0]['key']
            t = Movie.objects.get(movie_id=movie_id)
            t.youtube_id = youtube_id
            t.save()
            print(youtube_id)
        except:
            continue

# -------------------------- to save recommendation user-based in Customer collection ---------------------------

movie_obj = Customer.objects.get(user_id=request.user.id)
if movie_obj.rated >= 20:
    t_=get_recommendation(movie_obj.user.id)
    s = "|"
    s = s.join([str(k) for k in t_])
    movie_obj.recommendations=s
    movie_obj.save()
    print(s)
else:
    t_=get_popular()
    s = "|"
    s = s.join([str(k) for k in t_])
    movie_obj.recommendations = s
    movie_obj.save()
    print(s)
