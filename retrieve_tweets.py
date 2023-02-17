import tweepy
import pandas as pd
import configparser
import os

# Define file path and make sure path is correct
file_name = "config.ini"

# Config file stored in the same directory as the script.
# Get currect working directory with os.getcwd()
file_path = os.path.join(os.getcwd(), file_name)

# Read info from the config file named config.ini
config = configparser.RawConfigParser()
config.read(file_path)
token = config["twitter"]["Bearer_Token"]

# Initialize the client
client = tweepy.Client(bearer_token=token)

# The function takes in input the name of a trend and returns 30 tweets that contain it
# and returns a dataframe with the tweets
# The query start by the trend name, then we add -is:retweet to avoid retweets and finally lang:en

def get_tweets_trend(trend):
    try:
        query = trend + ' -is:retweet lang:en'
        tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=30)
        str_tweets = []

        for tweet in tweets.data:
            str_tweets.append(str(tweet))
            print(str(tweet))

        df_test = pd.DataFrame(str_tweets, columns=['tweet'])
        return df_test['tweet']
    except:
        print("Trend not found")

# Function very similar to the previous one, but it takes in input a username instead of a trend
# Instead of the trend name, we add from: to the query to specify that we want the tweets of a specific user
def get_tweets_user(user):
    try:
        query = 'from:' + user + ' -is:retweet lang:en'
        tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=30)
        str_tweets = []

        for tweet in tweets.data:
            str_tweets.append(str(tweet))

        df_test = pd.DataFrame(str_tweets, columns=['tweet'])
        return df_test['tweet']
    except:
        print("User not found")

