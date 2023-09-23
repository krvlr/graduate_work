#!/bin/bash

mongosh < /scripts/init_ugc.js
mongosh < /scripts/init_general_recommendations.js
# test
mongorestore --archive --gzip < /scripts/ugc_database.gz