#!/bin/bash

# Test script for course import API
# Usage: ./test_api.sh [URL] [TOKEN]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
API_URL="${1:-http://localhost:8000}"
IMPORT_TOKEN="${2:-${COURSE_IMPORT_TOKEN}}"
EXAMPLE_FILE="../examples/example-course.json"

# Check if token is provided
if [ -z "$IMPORT_TOKEN" ]; then
    echo -e "${RED}❌ Error: Import token is required${NC}"
    echo "Usage: ./test_api.sh [URL] [TOKEN]"
    echo "   or: export COURSE_IMPORT_TOKEN=your_token && ./test_api.sh"
    exit 1
fi

# Check if example file exists
if [ ! -f "$EXAMPLE_FILE" ]; then
    echo -e "${RED}❌ Error: Example file not found: $EXAMPLE_FILE${NC}"
    exit 1
fi

echo -e "${YELLOW}📤 Testing course import API${NC}"
echo "URL: $API_URL/api/import-course/"
echo "File: $EXAMPLE_FILE"
echo ""

# Send request
response=$(curl -s -w "\n%{http_code}" \
    -X POST "$API_URL/api/import-course/" \
    -H "X-Import-Token: $IMPORT_TOKEN" \
    -H "Content-Type: application/json" \
    -d @"$EXAMPLE_FILE")

# Split response and status code
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

echo -e "${YELLOW}📡 Response status: $http_code${NC}"
echo ""

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Success!${NC}"
    echo "$body" | python3 -m json.tool

    # Extract course slug
    course_slug=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('course_slug', ''))")
    admin_url=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('admin_url', ''))")

    if [ -n "$course_slug" ]; then
        echo ""
        echo -e "${GREEN}🔗 Preview URL:${NC} $API_URL/course/$course_slug/"
        echo -e "${GREEN}🔗 Admin URL:${NC} $API_URL$admin_url"
    fi
else
    echo -e "${RED}❌ Error!${NC}"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    exit 1
fi
