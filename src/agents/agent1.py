import requests
from uagents import Agent, Context,Model

# To receive messages to your Fetch.ai wallet (set to the Dorado testnet), enter your wallet address below:
MY_WALLET_ADDRESS = "fetch1___"

# Movie Database API URL and headers
MOVIES_API_URL1 = "https://moviesdatabase.p.rapidapi.com/titles/tt0000125"

headers = {
    'x-rapidapi-key': "ca01df7077mshfea6d79a8320efdp10da96jsn10b31a2749f8",
    'x-rapidapi-host': "moviesdatabase.p.rapidapi.com"
}
def get_movie_name() :
    responses = requests.get(MOVIES_API_URL1, headers= headers)
    if responses.status_code == 200:
        data = responses.json()
        if 'results' in data and data['results']:
            top_movie = data['results']
            return top_movie
    else:
        return None
# Initialize the agent
agent1 = Agent(name="agent1")

# Function to handle movie alerts based on threshold rating
@agent1.on_interval(period=5)
async def handle_movie_alert(ctx: Context):
    movie = get_movie_name()

    if movie:
        # ctx.logger.info(movie) --->to check data stored in movie.
        movie_name = movie['titleText']
        movie_year = movie['releaseYear']
        ctx.logger.info(f"The movie is {movie_name} relesed in {movie_year}")

        # Check if movie rating exceeds the threshold
        # if movie_rating > THRESHOLD_RATING:
        #     alert = f"The movie '{movie_title}' has a rating over the specified threshold: {movie_rating} > {THRESHOLD_RATING}"
        # else:
        #     alert = f"The movie '{movie_title}' has a rating back under the specified threshold: {movie_rating} < {THRESHOLD_RATING}"
        
        # Log the alert
#         ctx.logger.info(alert)

#         # Send alert to wallet address
#         if MY_WALLET_ADDRESS != "fetch1___":
#             await ctx.send_wallet_message(MY_WALLET_ADDRESS, alert)
#         else:
#             ctx.logger.info("To receive wallet alerts, set 'MY_WALLET_ADDRESS' to your wallet address.")
#     else:
#         ctx.logger.info("Failed to retrieve the top rated movie")

# # Run the agent
agent1.run()