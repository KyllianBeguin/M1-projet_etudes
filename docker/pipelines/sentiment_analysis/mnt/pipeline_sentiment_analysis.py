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

# Mongo specific errors
from pymongo.errors import BulkWriteError

# ===================================== PIPELINE =======================================
class PipelineSentimentAnalysis():
    """Perform sentiment analysis"""

    def __init__(self):
        self.client = None
        self.__endPipeline = False
        pass

    # ============================= PART 1 -- GET TWEETS ===============================
    def __connectToMongo(self) -> MongoClient:
        """Connect to mongo database"""
        host = "mongodb://mongo:27017"
        self.client = MongoClient(host)
        return None

    def __accessRawDataCollection(self):
        """Access to the Collection where are raw data"""
        self.__connectToMongo()
        db = self.client['TwitterSentimentAnalysis']
        collection = db['RawTweets']
        return collection

    @staticmethod
    def __getRawTweets(rawDataCollection):
        """Query the collection and return a list of tweets"""
        return [tweet for tweet in rawDataCollection.find({})]

    def RunGetTweets(self) -> list:
        """Run the Get tweets part and retun a list of tweets"""
        # Move to raw data collection
        collection = self.__accessRawDataCollection()

        # Get every tweets from raw data collection
        raw_tweets = self.__getRawTweets(collection)
        
        # Skip Mongo if no tweets in raw data collection
        if raw_tweets == []:
            self.__endPipeline = True
            return None
        return raw_tweets

    # ========================= PART 2 -- SENTIMENT ANALYSIS ===========================
    def __loadAfinn(self):
        """Load the sentiment analysis model"""
        self.afinn = Afinn()

    def __applyAfinn(self, tweet_text):
        """Return Positive or Negative based on Afinn score"""
        score = self.afinn.score(tweet_text)
        if score > 0:
            return 'Positive'
        else:
            return 'Negative'

    def RunSentimentAnalysis(self, raw_tweets: list[dict]):
        """Run the sentiment analysis part

        Args:
            raw_tweets (list[dict]) : content of each raw tweet
        """
        # End pipeline if no tweets to analyze
        if self.__endPipeline:
            return None

        # Load Afinn
        self.__loadAfinn()

        # Update content with sentiment analysis
        processed_tweets = [
            tweet |  {
                "Sentiment" : self.__applyAfinn(tweet["Tweet"])
            }
            for tweet
            in raw_tweets
        ]

        return processed_tweets

    # =========================== PART 3 -- PUSH TO MONGO ==============================
    @staticmethod
    def __removeRawTweets(rawDataCollection):
        """Clear Raw Tweets collection"""
        rawDataCollection.drop()
    
    def __accessProcessedCollection(self):
        """Access to the Collection where are processed data"""
        db = self.client['TwitterSentimentAnalysis']
        collection = db['ProcessedTweets']
        return collection

    @staticmethod
    def __pushTweetsCollection(processedTweetsCollection, processed_tweets):
        """Push the data in the collection

        Args:
            processedTweetsCollection (MongoCollection) : Collection where processed
                tweets are
            processed_tweets : date + text + sentiment of each tweet
        """
        processedTweetsCollection.insert_many(processed_tweets)

    def RunPushToMongo(self, processed_tweets):
        """Run the push part

        Args:
            processed_tweets : date + text + sentiment of each tweet
        """
        # Abort Push if __skipMongo
        if self.__endPipeline:
            return False

        # Move to processed data collection
        collection_processed = self.__accessProcessedCollection()

        # Remove Tweet id
        for tweet in processed_tweets:
            del tweet['Twitter_id']
        
        # Push processed tweets in Mongo
        self.__pushTweetsCollection(collection_processed, processed_tweets)

        # Clear the raw tweets collection
        collection_raw = self.__accessRawDataCollection()
        self.__removeRawTweets(collection_raw)
        
        return True
