# Zone d'import des bibliothèques
# Analyse de sentiment
from afinn import Afinn
# Connexion à la base de données
from pymongo import MongoClient
# Bibliothèque des dates
from datetime import datetime

# Zone de création des fonctions
def get_mongo_raw_tweets() -> list:
    """
    Fonction de récolte des tweets depuis la base mongodb

    Un Tweet est composé de
    * _id : l'id du tweet CHANGERA PROCHAINEMENT
    * Date : la date du tweet
    * Tweet : Le text du tweet

    :Retourne: une liste de Tweets
    """

    # Connextion à mongodb, bdd TweetsDB, Collection RawDataCollection
    host = "mongodb://mongo:27017"
    client = MongoClient(host)
    db = client['TweetsDB']
    collection = db['RawDataCollection']

    # Récolte de tous les tweets et stockage en liste
    raw_tweets = [tweet for tweet in collection.find()]

    return raw_tweets

def analyze_sentiments(tweets):
    """
    DOCUMENTER LA FONCTION
    """
    afinn = Afinn()
    analyzed_tweets = []
    for tweet in tweets:
        text = tweet['Tweet']
        sentiment_score = afinn.score(text)
        sentiment = 'Positive' if sentiment_score > 0 else 'Negative' if sentiment_score < 0 else 'Neutral'
        analyzed_tweet = {
            '_id': tweet['_id'],
            'Date': tweet['Date'],
            'Tweet': text,
            'Sentiment': sentiment
        }
        analyzed_tweets.append(analyzed_tweet)
    return analyzed_tweets

def mongo_export(list_tweets):
    """
    Export vers mongodb. 
    Base de données : TweetsDB 
    Collection : RawDataCollection
    """
    # Connect to host
    host = "mongodb://mongo:27017"
    client = MongoClient(host)

    # Access the desired database and collection
    db = client['TweetsDB']
    collection = db['ProcessedTweetsCollection']

    # Insert raw tweets
    collection.insert_many(list_tweets)

    # Close the connection
    client.close()

    return

# Analyze tweets
raw_tweets = get_mongo_raw_tweets()
analyzed_tweets = analyze_sentiments(raw_tweets)

# Run export
mongo_export(analyzed_tweets)