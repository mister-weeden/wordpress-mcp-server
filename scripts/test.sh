#!/bin/bash

echo "🧪 Testing WordPress MCP Server Connectivity"
echo "==========================================="

# Test WordPress API
echo "🔍 Testing WordPress REST API..."
if curl -s http://localhost:8888/wp-json/wp/v2/ | grep -q "namespace"; then
    echo "✅ WordPress REST API is working"
else
    echo "❌ WordPress REST API is not accessible"
    exit 1
fi

# Test MCP server connection
echo "🔍 Testing MCP server connection..."
if docker-compose exec -T wordpress-mcp-server wordpress-mcp-server --test-connection 2>/dev/null | grep -q "successful"; then
    echo "✅ MCP server can connect to WordPress"
else
    echo "❌ MCP server cannot connect to WordPress"
    echo "Check credentials in .env file"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
echo "🚀 Your WordPress MCP Server is ready for use with Claude!"
