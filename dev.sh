#!/bin/bash

# Script to run the project in development mode

echo "Starting development environment..."

# Copy dev environment file
cp .env.dev .env

# Run docker compose for development
docker compose up -d

echo ""
echo "Development environment started!"
echo "Access the application at: http://localhost:8000"
echo ""
echo "Useful commands:"
echo "  docker compose logs -f          # View logs"
echo "  docker compose down             # Stop containers"
echo "  docker compose exec web bash    # Access web container"
