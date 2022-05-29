import pandas as pd
import json
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_movie_ratings(movies: dict):
    ratings = pd.read_csv('dataset/ratings.csv')

    # extracting ratings for movies and storing in the movie dictionary
    for item, row in ratings.iterrows():
        movies[int(row["movieId"])]["ratings_val"] += int(row["rating"])
        movies[int(row["movieId"])]["ratings_total"] += 1


def get_movie_recommendation(movies: dict):
    data_matrix = {
        "movieId": [movie for movie in movies],
        "tags": [movies[movie]["tags"] for movie in movies],
    }

    data_matrix = pd.DataFrame(data_matrix)

    # converting movie tags into tokens
    cv = CountVectorizer(max_features=2000)
    movie_matrix = cv.fit_transform(data_matrix["tags"]).toarray()

    # calculating cosine similarity between movies
    # movie_similarity is a similarity matrix in which cell(i,j) represents
    # the cosine similarity between movie i and j such that 0 <= movie similarity <=1
    movie_similarity = cosine_similarity(movie_matrix)

    # finding top 50 similar movies to each movie
    for i in range(movie_similarity.shape[0]):
        # extracting movieId of ith movie
        print(i)
        idx = data_matrix.loc[i]
        movie_id = idx["movieId"]

        # extracting and sorting the similarity row (in descending order) of ith movie in similarity matrix
        distances = movie_similarity[i]
        distances = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

        # extracting top 51 recommendations for ith movie
        for k in range(51):
            if distances[k][0] == i:
                continue
            idx = data_matrix.loc[distances[k][0]]
            recc_id = idx["movieId"]
            movies[movie_id]["recommendations"].append(int(recc_id))


def format_tags(movies: dict):
    tags = pd.read_csv('dataset/tags.csv')

    # adding tags from tags.csv into each movie's tags
    for item, row in tags.iterrows():
        movies[int(row["movieId"])]["tags"].append(row["tag"].lower().replace(" ", ""))

    ps = PorterStemmer()
    for movie in movies:
        new_tags = []

        # stemming each tag using PortStemmer
        for text in movies[movie]["tags"]:
            new_tags.append(ps.stem(text))

        # joining all the tags as a string for each movie
        movies[movie]["tags"] = ' '.join([str(elem) for elem in new_tags])


def get_movie_data(movies: dict):
    items = pd.read_csv('dataset/movies.csv')

    for index, row in items.iterrows():
        # extracting release year of movie from title
        year = row["title"][-2:-6:-1][::-1]

        # extracting movie title
        movie_name = row["title"][:len(row["title"]) - 6]
        if movie_name[-1:-5:-1] == " ehT":
            movie_name = "The " + movie_name[:len(movie_name) - 5]

        # inserting values into the movies dictionary
        movies[int(row["movieId"])] = {
            "title": movie_name,
            "year": year,
            "genres": row["genres"].split(sep='|'),
            "tags": [i.lower().replace(" ", "") for i in row["genres"].split(sep='|')],
            "ratings_val": 0,
            "ratings_total": 0,
            "recommendations": []
        }


# for creating json of a dictionary and then writing the json data to a json file
def create_json(dictionary_name: dict, file_name: str):
    data_json = json.dumps(dictionary_name, indent=4)
    print(data_json)
    with open(f"json_files\{file_name}.json", "w") as outfile:
        outfile.write(data_json)


movies_data = {}  # dictionary to store movie data

get_movie_data(movies_data)
format_tags(movies_data)
get_movie_recommendation(movies_data)
get_movie_ratings(movies_data)

# create_json(movies_data, "movies_data")
print(movies_data[1])
# content based , popularity
