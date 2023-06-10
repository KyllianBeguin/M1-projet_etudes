import pandas as pd
import snscrape.modules.twitter as sntwitter
from datetime import date
from datetime import timedelta

# Build Query
date_today = date.today().__str__()
date_yesterday = date_today + timedelta(days=-1)
query = '#ReformeDesRetraites since:' + date_yesterday + ' until:' + date_today

# Set limit to 200 Tweets
limit = 200

# Scraping tweets
tweets = sntwitter.TwitterSearchScraper(query).get_items()

# Initialize tweets position's value
index = 0

# Initialize the list of dicts
dict_tweets = {}

# Excavating tweets
for tweet in tweets:
    if index == limit:
        break
    try:
        extract = {'Date': tweet.date, 'Tweet': tweet.rawContent}
    except KeyError:
        continue
    dict_tweets[index.__str__()] = extract
    index = index + 1