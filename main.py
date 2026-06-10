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
    height:500px;
    overflow:hidden;
    border-radius:20px;
    margin-bottom:30px;
    display:flex;
    align-items:center;
    justify-content:center;
}

.hero::before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    width:300%;
    height:100%;

    background:
    linear-gradient(rgba(0,0,0,.7),
    rgba(0,0,0,.8)),
    url("https://wallpapercave.com/wp/wp1945897.jpg");

    background-size:cover;
    background-repeat:repeat-x;

    animation:scrollBanner 40s linear infinite;
}

@keyframes scrollBanner{
0%{
transform:translateX(0);
}
100%{
transform:translateX(-66%);
}
}

.hero-content{
    position:relative;
    z-index:2;
    text-align:center;
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

.hero-btn{
    background:#E50914;
    color:white;
    padding:15px 35px;
    border-radius:8px;
    text-decoration:none;
    font-size:20px;
    font-weight:bold;
}

.hero-btn:hover{
    background:#b20710;
}

.hero button:hover{
    background:#b20710;
}
.movie-card{
    overflow:hidden;
    border-radius:12px;
    cursor:pointer;
    transition:0.4s;
    margin-bottom:10px;
}

.movie-card img{
    width:100%;
    border-radius:12px;
    transition:0.4s;
}

.movie-card:hover{
    transform:translateY(-10px) scale(1.08);
    box-shadow:0 20px 50px rgba(0,0,0,.8);
}

.movie-card:hover img{
    transform:scale(1.15);
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
st.markdown("""
<div class="hero">

<div class="hero-content">

<h1>
🎬 Unlimited Movies,<br>
TV Shows & More
</h1>

<p>
Discover Your Next Favorite Movie with AI 🤖
</p>

<a href="#search" class="hero-btn">
🍿 Get Recommendations
</a>

<div class="tagline">
Powered by Machine Learning • 5000+ Movies • Personalized Picks
</div>

</div>

</div>
""", unsafe_allow_html=True)
# -------------------------
# SEARCH
# -------------------------

st.markdown('<div id="search"></div>', unsafe_allow_html=True)

selected_movie = st.selectbox(
    "🔍 Search Movie",
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

            st.markdown(
    f"""
    <div class="movie-card">
        <img src="{poster}">
    </div>
    """,
    unsafe_allow_html=True
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

                "▶ Movie Trailer",

                trailer

                )

            st.link_button(

            "🎬 Movie Info",

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

            st.markdown(
    f"""
    <div class="movie-card">
        <img src="{poster}">
    </div>
    """,
    unsafe_allow_html=True
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
                    "▶ Movie Trailer",
                    trailer
                )

            st.link_button(
                "🎬 Movie Info",
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

            st.markdown(
    f"""
    <div class="movie-card">
        <img src="{poster}">
    </div>
    """,
    unsafe_allow_html=True
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
                    "▶ Movie Trailer",
                    trailer
                )

            st.link_button(
                "🎬 Movie Info",
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