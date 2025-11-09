#!/bin/bash

# Script to initialize Let's Encrypt SSL certificates for the first time
# Usage: ./init-ssl.sh your-domain.com your-email@example.com

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./init-ssl.sh <domain> <email>"
    echo "Example: ./init-ssl.sh example.com admin@example.com"
    exit 1
fi

DOMAIN=$1
EMAIL=$2

echo "========================================="
echo "Initializing SSL certificates for:"
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo "========================================="

# Create directories if they don't exist
mkdir -p certbot/conf certbot/www

# Stop nginx temporarily
echo "Stopping nginx..."
docker compose -f docker-compose.production.yml stop nginx

# Request certificate
echo "Requesting SSL certificate from Let's Encrypt..."
docker compose -f docker-compose.production.yml run --rm certbot certonly \
  --standalone \
  -d $DOMAIN \
  -d www.$DOMAIN \
  --email $EMAIL \
  --agree-tos \
  --no-eff-email \
  --force-renewal

echo "========================================="
echo "SSL certificates obtained successfully!"
echo "========================================="

echo ""
echo "Next steps:"
echo "1. Edit nginx/conf.d/app.conf"
echo "2. Uncomment SSL configuration lines"
echo "3. Replace 'yourdomain.com' with '$DOMAIN'"
echo "4. Comment out the 'Temporary HTTP-only server' block"
echo "5. Restart nginx: docker compose -f docker-compose.production.yml up -d nginx"
echo ""
echo "Or run: nano nginx/conf.d/app.conf"
