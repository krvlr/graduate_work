SHELL = /bin/sh
CURRENT_UID := $(shell id -u)

mongo_setup:
	docker exec -it mongo bash -c "cat /scripts/init_mongo.js | mongosh"