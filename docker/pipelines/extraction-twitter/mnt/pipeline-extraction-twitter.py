from typing import Optional

import requests


def do_work(data: dict) -> None:
    # do actual work with data
    print(data["date"], "\n", data["text"])


def do_request(tweet_id) -> Optional[dict]:
    response = requests.get(url=f"https://api.vxtwitter.com/Twitter/status/{tweet_id}")
    if not response.ok:
        print("Couldn't get tweet.")
        return
    try:
        do_work(response.json())
    except requests.JSONDecodeError:
        print("Couldn't decode response.")
        return

try:
	from googlesearch import search
except ImportError:
	print("No module named 'google' found")

# Get last day date
from datetime import datetime
from datetime import timedelta
yesterday = datetime.today() - timedelta(days=1)

# to search
query = f'"réforme des retraites" site:twitter.com after:{yesterday.strftime("%Y-%m-%d")}'

tweet_ids = []

for link in search(query, tld="co.in", num=10, stop=20, pause=2):
    tweet_url_parts = link.split("/")
    tweet_id = tweet_url_parts[-1]
    try :
        int(tweet_id)
        tweet_ids.append(tweet_id)
    except ValueError:
        pass

for i, tweet_id in enumerate(tweet_ids, start=1):
    do_request(tweet_id)
    # print(f"Tweet {i}: {tweet_id}")
