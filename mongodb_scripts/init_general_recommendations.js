const dbname = "general_recommendations";
const conn = new Mongo();
const database = conn.getDB(dbname);

movies_collection = "movies";
database.createCollection(movies_collection);
database[movies_collection].createIndex({["movie_id"]: -1});
database[movies_collection].createIndex({["rating"]: -1});

use admin;
database.createUser({
  user: "default_general_recommendations",
  pwd:  "default_password",
  roles: [{ role:"readWrite", db:`${dbname}`}],
  mechanisms: [ "SCRAM-SHA-256" ],
});