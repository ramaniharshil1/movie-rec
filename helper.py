import requests

API_KEY = "9d24e325cd54312858c3323297acd296"


def fetch_poster(movie_id):

    try:

        movie_id = int(movie_id)

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

        response = requests.get(url)

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:

            return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception as e:

        print(e)

    return "https://via.placeholder.com/300x450?text=No+Poster"


def get_trailer(movie_id):

    try:

        movie_id = int(movie_id)

        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

        response = requests.get(url)

        data = response.json()

        for video in data.get("results", []):

            if video["site"] == "YouTube":

                return f"https://www.youtube.com/watch?v={video['key']}"

    except Exception as e:

        print(e)

    return None