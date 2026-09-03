#!/bin/bash
set -e

CONTAINER_NAME="demo-mysql"
DB_NAME="demoapp"
DB_ROOT_PASSWORD="root"

echo "Checking MySQL container..."

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "MySQL container already running."
elif [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Starting existing MySQL container..."
    docker start $CONTAINER_NAME
else
    echo "Creating new MySQL container..."
    docker run --name $CONTAINER_NAME \
        -e MYSQL_ROOT_PASSWORD=$DB_ROOT_PASSWORD \
        -e MYSQL_DATABASE=$DB_NAME \
        -p 3306:3306 \
        -d mysql:8
fi

echo "Waiting for MySQL to be ready..."
until docker exec $CONTAINER_NAME mysqladmin ping -h 127.0.0.1 -uroot -p$DB_ROOT_PASSWORD --silent > /dev/null 2>&1; do
    sleep 1
    echo -n "."
done
echo ""
echo "MySQL is ready."

echo "Applying schema..."
docker exec -i $CONTAINER_NAME mysql -uroot -p$DB_ROOT_PASSWORD $DB_NAME < schema.sql

echo "Launching app..."
python3 src/main.py