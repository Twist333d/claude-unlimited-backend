# scripts/sanity_check.sh

#!/bin/bash

API_URL="${APP_BASE_URL:-http://localhost:5000}"
TOKEN=$(python -c "from app.tests.smoke_tests import get_test_token; print(get_test_token())")

echo "Running sanity checks against $API_URL"

# Health check
health_check=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health)
if [ $health_check == "200" ]; then
    echo "✅ API health check passed"
else
    echo "❌ API health check failed"
    exit 1
fi

# Chat functionality check
chat_response=$(curl -s -X POST $API_URL/chat \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"message":"Hello, Claude!"}')

if [[ $chat_response == *"response"* ]]; then
    echo "✅ Chat functionality check passed"
else
    echo "❌ Chat functionality check failed"
    exit 1
fi

echo "All sanity checks passed!"