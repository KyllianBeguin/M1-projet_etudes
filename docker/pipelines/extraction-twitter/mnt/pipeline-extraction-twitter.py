import pandas as pd
# import nest_asyncio
import snscrape.modules.twitter as sntwitter
from snscrape.base import ScraperException

query = '#ReformeDesRetraites since:2023-03-01 until:2023-06-09'
limit = 100

tweets = sntwitter.TwitterSearchScraper(query).get_items()

index = 0
df = pd.DataFrame(columns=['Date','Tweet'])

for tweet in tweets:
    if index == limit:
        break
    try:
        df2 = {'Date': tweet.date, 'Tweet': tweet.rawContent}
    except KeyError:
        continue
    df = pd.concat([df, pd.DataFrame.from_records([df2])])
    index = index + 1

df.to_csv('tweets.csv')