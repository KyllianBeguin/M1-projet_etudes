# snscrape for Twitter scraping
import snscrape.modules.twitter as sntwitter

# Datetime to build the query
from datetime import date
from datetime import timedelta

# MongoClient to export to MongoDB
from pymongo import MongoClient

# Build Query
date_today = date.today()
date_yesterday = date_today + timedelta(days=-1)
query = '#ReformeDesRetraites since:' + date_yesterday.__str__() + ' until:' + date_today.__str__()

# Set limit to 200 Tweets
limit = 200

# Scraping tweets
tweets = sntwitter.TwitterSearchScraper(query).get_items()

# Initialize tweets position's value
index = 0

# Initialize the list of dicts
list_tweets = []

# Excavating tweets
for tweet in tweets:
    if index == limit:
        break
    try:
        extract = {'Date': tweet.date, 'Tweet': tweet.rawContent}
    except KeyError:
        continue
    list_tweets.append(extract)
    index = index + 1

# Export to mongodb. TweetsDB database, RawDataCollection
# Connect to host
host = "mongodb://mongo:27017"
client = MongoClient(host)

# Access the desired database and collection
db = client['TweetsDB']
collection = db['RawDataCollection']

# Insert raw tweets
collection.insert_many(list_tweets)

# Close the connection
client.close()