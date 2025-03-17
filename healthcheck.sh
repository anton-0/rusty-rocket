#!/bin/bash

# Checks if postgress is ready to accept connections.

for ((i=0; i<10; i++)); do
    OUTPUT=$(docker exec -it postgres pg_isready -U $POSTGRES_USER -d $POSTGRES_DB 2>&1)
    [[ $OUTPUT =~ "accepting connections" ]] && exit 0

    sleep 1
done

exit 1