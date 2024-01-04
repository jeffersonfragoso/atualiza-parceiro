#!/bin/bash

set -e
set -u

function create_user_and_database() {
	local database=$1
	echo "Creating user and database '$database'"
	psql -v ON_ERROR_STOP=1 --username "$DB_USER" <<-EOSQL
	    CREATE USER $database PASSWORD '$database';
	    CREATE DATABASE $database;
	    GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL
}

if [ -n "$DB_NAME" ]; then
	echo "Creating DB(s): $DB_NAME"
	for db in $(echo $DB_NAME | tr ',' ' '); do
		create_user_and_database $db
	done
	echo "Multiple databases created"
fi
