FROM mongo:7.0-rc

COPY mnt/mongo_setup.js /docker-entrypoint-initdb.d/mongo_setup.js

CMD [ "mongod" ]