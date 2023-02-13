import tweepy
import pandas as pd

# Inizializzazione del client di tweepy tramite il bearer token
token=''
client = tweepy.Client(bearer_token=token)

# Funzione che prende in ingresso il nome di un trend e restituisce 30 tweet che ne fanno parte in dataframe
# Tramite il client di tweepy vengono effettuate le query
# La query è composta dal nome del trend, -is:retweet indica che non vogliamo retweet e infine lang:en
# indica che vogliamo solo tweet in inglese

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

# Funzione che prende in ingresso il nome di un utente e restituisce 30 tweet che ne fanno parte in dataframe
# A differenza dell'altra funzione in questo caso usiamo "from:" per indicare che vogliamo i tweet di un utente
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


