db = new Mongo().getDB('RawDataDB');

db.createCollection('RawTweetsCollection');