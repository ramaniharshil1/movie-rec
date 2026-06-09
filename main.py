import streamlit as st
import pickle
import requests
from helper import fetch_poster,get_trailer

# -------------------------
# CONFIG
# -------------------------

st.set_page_config(
    page_title="Netflix",
    page_icon="🎬",
    layout="wide"
)

API_KEY="9d24e325cd54312858c3323297acd296"

# -------------------------
# CSS
# -------------------------

st.markdown("""
<style>

.stApp{
background:#141414;
}

.netflix{
color:#E50914;
font-size:55px;
font-weight:bold;
}

.hero{
padding:40px;
background:#000;
border-radius:15px;
margin-bottom:20px;
}

.hero h1{
color:white;
font-size:55px;
}

.hero p{
color:white;
font-size:18px;
}

h1,h2,h3,h4,h5{
color:white !important;
}

.stButton button{
background:#E50914;
color:white;
width:100%;
border:none;
}

</style>
""",unsafe_allow_html=True)

# -------------------------
# LOAD
# -------------------------

movies=pickle.load(
open("movies.pkl","rb")
)

similarity=pickle.load(
open("similarity.pkl","rb")
)

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("NETFLIX")
# -------------------------
# HEADER
# -------------------------
import streamlit as st

# Hero Section
st.markdown("""
<style>

.netflix{
    color:#E50914;
    font-size:50px;
    font-weight:900;
    text-align:center;
    letter-spacing:3px;
    margin-bottom:20px;
    font-family:Arial;
}

.hero{
    position:relative;
    background:
    linear-gradient(rgba(0,0,0,0.75),
    rgba(0,0,0,0.85)),
    url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1600");
    background-size:cover;
    background-position:center;
    border-radius:20px;
    padding:100px 50px;
    text-align:center;
    margin-bottom:30px;
    box-shadow:0px 10px 30px rgba(0,0,0,0.5);
}

.hero h1{
    color:white;
    font-size:65px;
    font-weight:900;
    line-height:1.1;
    margin-bottom:20px;
}

.hero p{
    color:#d1d5db;
    font-size:24px;
    margin-bottom:30px;
}

.hero button{
    background:#E50914;
    color:white;
    border:none;
    padding:15px 40px;
    font-size:20px;
    font-weight:bold;
    border-radius:8px;
    cursor:pointer;
}

.hero button:hover{
    background:#b20710;
}

.tagline{
    color:#facc15;
    font-size:18px;
    font-weight:600;
    margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

# Netflix Logo
st.markdown(
    '<div class="netflix">NETFLIX</div>',
    unsafe_allow_html=True
)

# Hero Poster
st.markdown("""
<div class="hero">

<h1>
🎬 Unlimited Movies,<br>
TV Shows & More
</h1>

<p>
Discover Your Next Favorite Movie with AI 🤖
</p>

<button>
🍿 Get Recommendations
</button>

<div class="tagline">
Powered by Machine Learning • 5000+ Movies • Personalized Picks
</div>

</div>
""", unsafe_allow_html=True)

# -------------------------
# SEARCH
# -------------------------

selected_movie=st.selectbox(

"Search Movie",

movies["title"].values

)

# -------------------------
# RECOMMEND
# -------------------------

def recommend(movie):

    index=movies[
    movies["title"]==movie
    ].index[0]

    distances=similarity[index]

    movie_list=sorted(

    list(
    enumerate(
    distances
    )
    ),

    reverse=True,

    key=lambda x:x[1]

    )[1:6]

    names=[]
    posters=[]
    ratings=[]
    years=[]
    ids=[]

    for i in movie_list:

        ids.append(
        movies.iloc[i[0]]["id"]
        )

        names.append(
        movies.iloc[i[0]]["title"]
        )

        posters.append(
        fetch_poster(
        movies.iloc[i[0]]["id"]
        )
        )

        ratings.append(
        movies.iloc[i[0]]["vote_average"]
        )

        years.append(
        str(
        movies.iloc[i[0]]
        ["release_date"]
        )[:4]
        )

    return ids,names,posters,ratings,years

# -------------------------
# BUTTON
# -------------------------

if st.button(
"🎬 Recommend Movies"
):

    ids,names,posters,ratings,years=\
    recommend(
    selected_movie
    )

    cols=st.columns(5)

    for col,movie_id,name,poster,rating,year in zip(

    cols,
    ids,
    names,
    posters,
    ratings,
    years

    ):

        with col:

            st.image(

            poster,

            use_container_width=True

            )

            st.write(
            name
            )

            st.write(
            "⭐",rating
            )

            st.write(
            "📅",year
            )

            trailer=get_trailer(
            movie_id
            )

            if trailer:

                st.link_button(

                "▶ Trailer",

                trailer

                )

            st.link_button(

            "🎬 Details",

            f"https://www.themoviedb.org/movie/{movie_id}"

            )
            # -----------------------------------
# TRENDING MOVIES
# -----------------------------------

st.markdown("---")
st.subheader("🔥 Trending Movies")

url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={"9d24e325cd54312858c3323297acd296"}"

response = requests.get(url)

data = response.json()

if "results" in data:

    results = data["results"][:5]

    cols = st.columns(5)

    for col, movie in zip(cols, results):

        with col:

            poster = (
                "https://image.tmdb.org/t/p/w500"
                + movie["poster_path"]
            )

            st.image(
                poster,
                use_container_width=True
            )

            st.write(movie["title"])

            st.write(
                f"⭐ {movie['vote_average']}"
            )

            trailer = get_trailer(
                movie["id"]
            )

            if trailer:

                st.link_button(
                    "▶ Trailer",
                    trailer
                )

            st.link_button(
                "🎬 More Info",
                f"https://www.themoviedb.org/movie/{movie['id']}"
            )

            # -----------------------------------
# POPULAR MOVIES
# -----------------------------------

st.markdown("---")
st.subheader("⭐ Popular Movies")

url = f"https://api.themoviedb.org/3/movie/popular?api_key={"9d24e325cd54312858c3323297acd296"}"

response = requests.get(url)

data = response.json()

if "results" in data:

    results = data["results"][:5]

    cols = st.columns(5)

    for col, movie in zip(cols, results):

        with col:

            poster = (
                "https://image.tmdb.org/t/p/w500"
                + movie["poster_path"]
            )

            st.image(
                poster,
                use_container_width=True
            )

            st.write(movie["title"])

            st.write(
                f"⭐ {movie['vote_average']}"
            )

            trailer = get_trailer(
                movie["id"]
            )

            if trailer:

                st.link_button(
                    "▶ Trailer",
                    trailer
                )

            st.link_button(
                "🎬 More Info",
                f"https://www.themoviedb.org/movie/{movie['id']}"
            )


st.sidebar.markdown("---")

st.sidebar.button("🏠 Home")

st.sidebar.button("🔥 Trending")

st.sidebar.button("⭐ Popular")

st.sidebar.button("🎬 Movies")

st.sidebar.button("❤️ My List")

st.sidebar.markdown("---")

st.sidebar.info(
"""
Movie Recommendation System

Machine Learning

TMDB API
"""
)
st.sidebar.write("Harshil Ramani")