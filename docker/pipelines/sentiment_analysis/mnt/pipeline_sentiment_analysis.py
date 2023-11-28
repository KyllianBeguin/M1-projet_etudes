# ====================================== ABOUT =========================================
"""
Name : Pipeline - Sentiment Analysis
Authors : Hortense CAMELIN, Kyllian BEGUIN
Project : Sentiment Analysis - M1 Big Data
"""

# ===================================== IMPORTS ========================================
# To perform sentiment analysis
from afinn import Afinn

# Interact with mongo
from pymongo import MongoClient

# TODO : why datetime?
from datetime import datetime

# ===================================== PIPELINE =======================================
class PipelineSentimentAnalysis():
    """Perform sentiment analysis"""

    def __init__(self):
        pass
    # ============================= PART 1 -- GET TWEETS ===============================
    def __connectToMongo(self) -> MongoClient:
        """Connect to mongo database"""
        host = "mongodb://mongo:27017"
        client = MongoClient(host)
        return client

    def __accessRawDataCollection(self):
        """Access to the Collection where are raw data"""
        client = self.__connectToMongo()
        db = client['TweetsDB']
        collection = db['RawDataCollection']
        return collection

    @staticmethod
    def __getRawTweets(rawDataCollection):
        """Query the collection and return a list of tweets"""
        return [tweet for tweet in rawDataCollection.find()]

    def RunGetTweets(self) -> list:
        """Run the Get tweets part and retun a list of tweets"""

    # ========================= PART 2 -- SENTIMENT ANALYSIS ===========================

    # ===================== PART 3 -- CLEAR RAW DATA COLLECTION ========================

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
