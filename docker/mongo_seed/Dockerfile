FROM mongo:7.0-rc
COPY ./mnt/ProcessedTweetsCollection.json .
CMD mongoimport --host mongo --db TwitterSentimentAnalysis --collection ProcessedTweets --type json --file ./ProcessedTweetsCollection.json
