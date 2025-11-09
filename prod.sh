#!/bin/bash

# Script to run the project in production mode

echo "Starting production environment..."

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "ERROR: .env.prod file not found!"
    echo "Please create .env.prod with your production settings."
    echo "You can use .env.example as a template."
    exit 1
fi

# Copy prod environment file
cp .env.prod .env

# Run docker compose for production
docker compose -f docker-compose.production.yml up -d

echo ""
echo "Production environment started!"
echo ""
echo "Useful commands:"
echo "  docker compose -f docker-compose.production.yml logs -f          # View logs"
echo "  docker compose -f docker-compose.production.yml down             # Stop containers"
echo "  docker compose -f docker-compose.production.yml exec web bash    # Access web container"
