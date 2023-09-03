FROM mongo:7.0-rc
COPY ./mnt/ProcessedTweetsCollection.json .
CMD mongoimport --host mongo --db RawDataDB --collection ProcessedTweetsCollection --type json --file ./ProcessedTweetsCollection.json