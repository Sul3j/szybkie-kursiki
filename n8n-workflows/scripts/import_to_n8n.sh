#!/bin/bash

# Import workflow to n8n via API
# Usage: ./import_to_n8n.sh [n8n_api_key]

set -e

WORKFLOW_FILE="../course-generator-workflow.json"
N8N_URL="https://n8n.szybkie-kursiki.pl"
N8N_API_KEY="${1:-${N8N_API_KEY}}"

if [ -z "$N8N_API_KEY" ]; then
    echo "❌ Error: n8n API key required"
    echo "Usage: ./import_to_n8n.sh YOUR_API_KEY"
    echo "   or: export N8N_API_KEY=your_key && ./import_to_n8n.sh"
    echo ""
    echo "Get your API key from: $N8N_URL/settings/api"
    exit 1
fi

if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "❌ Error: Workflow file not found: $WORKFLOW_FILE"
    exit 1
fi

echo "📤 Importing workflow to n8n..."
echo "URL: $N8N_URL"
echo "File: $WORKFLOW_FILE"
echo ""

response=$(curl -s -w "\n%{http_code}" \
    -X POST "$N8N_URL/api/v1/workflows" \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Content-Type: application/json" \
    -d @"$WORKFLOW_FILE")

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
    echo "✅ Workflow imported successfully!"
    echo "$body" | python3 -m json.tool

    workflow_id=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
    if [ -n "$workflow_id" ]; then
        echo ""
        echo "🔗 Open workflow: $N8N_URL/workflow/$workflow_id"
    fi
else
    echo "❌ Error importing workflow (HTTP $http_code)"
    echo "$body"
    exit 1
fi
