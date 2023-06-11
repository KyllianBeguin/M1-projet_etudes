db = new Mongo().getDB('RawDataDB');

db.createCollection('RawTweetsCollection');

db.createCollection('ProcessedTweetsCollection');