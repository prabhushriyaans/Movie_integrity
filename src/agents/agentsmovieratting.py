import requests
from uagents import Agent, Context, Model

# To receive messages to your Fetch.ai wallet (set to the Dorado testnet), enter your wallet address below:
MY_WALLET_ADDRESS = "fetch1___"

# Movie Database API URL and headers
MOVIES_API_URL = "https://moviesdatabase.p.rapidapi.com/titles/tt0000125/ratings"
headers = {
    'x-rapidapi-key': "ca01df7077mshfea6d79a8320efdp10da96jsn10b31a2749f8",
    'x-rapidapi-host': "moviesdatabase.p.rapidapi.com"
}

MOVIES_API_URL1 = "https://moviesdatabase.p.rapidapi.com/titles/tt0000125"

headers1 = {
    'x-rapidapi-key': "ca01df7077mshfea6d79a8320efdp10da96jsn10b31a2749f8",
    'x-rapidapi-host': "moviesdatabase.p.rapidapi.com"
}

def get_movie_name():
    response = requests.get(MOVIES_API_URL1, headers=headers1)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            movie_info = data['results']  # Select the first result
            # Extracting movie title and year
            movie_title = movie_info['titleText']['text']
            movie_year = movie_info['releaseYear']['year']
            return movie_title, movie_year
    return None, None

# Initialize the agent
agent1 = Agent(name="agent1")

# Function to handle movie alerts based on threshold rating
@agent1.on_interval(period=5)
async def handle_movie_alert(ctx: Context):
    movie_title, movie_year = get_movie_name()

    if movie_title and movie_year:
        ctx.logger.info(f"The movie is {movie_title} released in {movie_year}")
    else:
        ctx.logger.info("Failed to retrieve movie information.")

# Threshold rating for movie alerts
THRESHOLD_RATING = 2.0

# Function to fetch the top rated movie
def get_top_rated_movie():
    response = requests.get(MOVIES_API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            top_movie = data['results']
            return top_movie
    else:
        return None

# Initialize the agent
agent2 = Agent(name="agent2")

# Function to handle movie alerts based on threshold rating
@agent2.on_interval(period=5)
async def handle_movie_alert(ctx: Context):
    movie = get_top_rated_movie()

    if movie:
        # ctx.logger.info(movie) --->to check data stored in movie.
        movie_rating = movie['averageRating']
        movie_votes = movie['numVotes']
        ctx.logger.info(f"The movie has rating of {movie_rating} with {movie_votes} votes")

        # Send alert to wallet address
        if MY_WALLET_ADDRESS != "fetch1___":
            await ctx.send_wallet_message(MY_WALLET_ADDRESS, alert)
        else:
            ctx.logger.info("To receive wallet alerts, set 'MY_WALLET_ADDRESS' to your wallet address.")
    else:
        ctx.logger.info("Failed to retrieve the top rated movie")

#Run the agent
agent2.run()
agent1.run()