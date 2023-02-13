import joblib
import pickle
from pre_processing_text import denoise_text
import sys

# Load the model
current_path = sys.path[0]
filename = current_path + "/naive_bayes.joblib"
loaded_model = joblib.load(filename)

# Load the vectorizer
filename = current_path + "/vectorizer.pickle"
Tfidf_vect = pickle.load(open(filename, "rb"))


# Predict the label of a single tweet
def predict(messagge):
    messagge = denoise_text(messagge)
    messagge= Tfidf_vect.transform([messagge])
    y_predicted = loaded_model.predict(messagge)
    return y_predicted

# Predict the label of a list of tweets given as input a dataframe of tweets
def predict_tweets(tweets):
    tweets = tweets.apply(denoise_text)
    tweets= Tfidf_vect.transform(tweets)
    y_predicted = loaded_model.predict(tweets)
    return y_predicted
