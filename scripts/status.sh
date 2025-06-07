#!/bin/bash

echo "📊 WordPress MCP Server - Status Check"
echo "====================================="

# Check if services are running
echo "🔍 Service Status:"
docker-compose ps

echo ""
echo "🌐 Connection Tests:"

# Test WordPress
if curl -s -I http://localhost:8888 | grep -q "200 OK"; then
    echo "✅ WordPress is accessible at http://localhost:8888"
else
    echo "❌ WordPress is not accessible"
fi

# Test MCP server (if running in HTTP mode)
if curl -s http://localhost:9001/health &>/dev/null; then
    echo "✅ MCP Server HTTP is accessible at http://localhost:9001"
else
    echo "ℹ️  MCP Server HTTP not accessible (normal if using stdio mode)"
fi

# Test database connection
if docker-compose exec -T bedrock-db mysqladmin ping -h localhost --silent 2>/dev/null; then
    echo "✅ Database is accessible"
else
    echo "❌ Database is not accessible"
fi

echo ""
echo "📈 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "💾 Volume Usage:"
docker system df

echo ""
echo "🔧 Quick Actions:"
echo "./logs.sh [service]  - View logs"
echo "./backup.sh          - Create backup"
echo "./reset.sh           - Reset everything"
