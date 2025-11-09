#!/bin/bash

set -e

echo "========================================="
echo "Starting deployment process..."
echo "========================================="

# Navigate to project directory
cd /home/deploy/szybkie-kursiki || exit 1

# Pull latest changes from GitHub
echo "Pulling latest changes from GitHub..."
git pull origin main

# Build and restart containers
echo "Building Docker containers..."
docker compose -f docker-compose.production.yml build --no-cache

echo "Stopping old containers..."
docker compose -f docker-compose.production.yml down

echo "Starting new containers..."
docker compose -f docker-compose.production.yml up -d

# Wait for containers to start
echo "Waiting for containers to start..."
sleep 10

# Run migrations
echo "Running database migrations..."
docker compose -f docker-compose.production.yml exec -T web python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
docker compose -f docker-compose.production.yml exec -T web python manage.py collectstatic --noinput

# Clean up unused Docker resources
echo "Cleaning up Docker resources..."
docker system prune -f

echo "========================================="
echo "Deployment completed successfully!"
echo "========================================="

# Show running containers
docker compose -f docker-compose.production.yml ps
