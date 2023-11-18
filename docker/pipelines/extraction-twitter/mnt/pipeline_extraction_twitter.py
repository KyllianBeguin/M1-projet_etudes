# ======================================= ABOUT ==========================================
"""
Name : Pipeline - Extraction Twitter
Author : Kyllian BEGUIN
Project : Sentiment Analysis - M1 Big Data
"""

# ===================================== IMPORTS ========================================
# To query api.vxtwitter.com
import requests

# To query Google
from datetime import datetime
from datetime import timedelta
from googlesearch import search

# To push to Mongo
from pymongo import MongoClient

# ===================================== PIPELINE =======================================
class PipelineExtractionTwitter():
    """Scrap Tweets

    Attributes :
        query(str) : query to send to Google
    """
    def __init__(self):
        # To build Query
        self.__query = None
        # To skip PushToMongo
        self.__skipMongo = False

    # ========================= PART 1 -- TWITTER EXTRACTION ===========================
    @staticmethod
    def __buildYesterdayDate() -> str:
        """Returns previous date as a string"""
        yesterday = datetime.today() - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def __buildQuery(self, topic : str):
        """Takes a topic and return a query used by google library

        Args:
            topic (str) : The topic to scrap
        """
        yesterday = self.__buildYesterdayDate
        site = "twitter.com"
        self.__query = (
            f'"{topic}"'
            f' site:{site}'
            f' after:{yesterday}'
        )
        return None

    def __queryGoogle(self) -> list[str]:
        """Query Google and returns a list of tweet id"""
        # Perform the query
        links = search(
            self.__query
            , tld="co.in"
            , num=10
            , stop=20
            , pause=2
        )

        # Initialize list of tweet id
        tweets_id = []

        # Process links to get tweet ids
        for link in links:
            tweet_url_parts = link.split("/")
            tweet_id = tweet_url_parts[-1]
            # Ensure the last part is an id (numeric)
            try :
                int(tweet_id)
                tweets_id.append(tweet_id)
            except ValueError:
                 pass

        return tweets_id

    @staticmethod
    def __getTweetsContent(tweets_id : list[str]) -> list[dict]:
        """Query api.vxtwitter.com and return date + text of the tweet

        Args:
            tweets_id (list[str]) : The list of tweet ids
        """
        # Initialize tweets content
        tweets_content = []

        for tweet_id in tweets_id:
            url = f"https://api.vxtwitter.com/Twitter/status/{tweet_id}" 
            response = requests.get(url = url)
            if not response.ok:
                print("Couldn't get tweet.")
                return None
            try:
                content = {
                    "Date" : response.json()["date"]
                    , "Tweet" : response.json()["text"]
                }
                tweets_content.append(content)
            except requests.JSONDecodeError:
                print("Couldn't decode response.")
                return None
        
        return tweets_content

    def RunTwitterExtraction(self, topic : str) -> list[dict]:
        """Run the extraction part and return the data

        Args:
            topic (str) : The topic to scrap
        """
        # Build query
        self.__buildQuery(topic)

        # Query Google
        tweets_id = self.__queryGoogle()

        if len(tweets_id) == 0:
            self.__skipMongo = True
            return None

        # Get Content
        tweets_content = self.__getTweetsContent(tweets_id = tweets_id)
        return tweets_content

    # =========================== PART 2 -- PUSH TO MONGO ==============================
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
    def __pushTweetsContent(rawDataCollection, tweets_content : list[dict]):
        """Push the data in the collection

        Args:
            rawDataCollection (MongoCollection) : Collection where raw tweets are
            tweets_content (list[dict]) : date + text of each tweet
        """
        rawDataCollection.insert_many(tweets_content)
        return None

    def RunPushToMongo(self, tweets_content : list[dict]):
        """Run the push part

        Args:
            tweets_content (list[dict]) : date + text of each tweet
        """
        # Abort Push if __skipMongo
        if self.__skipMongo:
            return False
        # Move to raw data collection
        collection = self.__accessRawDataCollection()

        # Push Tweets in the collection
        self.__pushTweetsContent(
            rawDataCollection = collection
            , tweets_content = tweets_content
        )

        return True

