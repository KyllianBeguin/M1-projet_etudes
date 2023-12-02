db = new Mongo().getDB('TwitterSentimentAnalysis');

db.createCollection('RawTweets');

db.createCollection('ProcessedTweets');
