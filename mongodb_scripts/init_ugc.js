const dbname = "ugc";
const conn = new Mongo();
const database = conn.getDB(dbname);

rating_collection = "rating";
database.createCollection(rating_collection);
database[rating_collection].createIndex({["movie_id"]: -1});
database[rating_collection].createIndex({["rating"]: -1});

reviews_collection = "review";
database.createCollection(reviews_collection);
database[reviews_collection].createIndex({["movie_id"]: -1});

bookmark_collection = "bookmark";
database.createCollection(bookmark_collection);
database[bookmark_collection].createIndex({["movie_id"]: -1});

progress_collection = "progress";
database.createCollection(progress_collection);
database[progress_collection].createIndex({["movie_id"]: -1});

use admin;
database.createUser({
  user: "default_ugc",
  pwd:  "default_password",
  roles: [{ role:"readWrite", db:`${dbname}`}],
  mechanisms: [ "SCRAM-SHA-256" ],
});