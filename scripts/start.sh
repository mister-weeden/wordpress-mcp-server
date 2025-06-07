#!/bin/bash
set -e

echo "🚀 Starting WordPress MCP Server Stack"
echo "======================================"

# Default mode
MODE=${1:-default}

case $MODE in
    "default")
        echo "🔧 Starting default stack (stdio mode for Claude Desktop)..."
        docker-compose up -d bedrock-db bedrock wordpress-mcp-server
        ;;
    "http")
        echo "🌐 Starting with HTTP MCP server..."
        docker-compose --profile http up -d
        ;;
    "production")
        echo "🏭 Starting production stack with Nginx..."
        docker-compose --profile production up -d
        ;;
    *)
        echo "❌ Invalid mode: $MODE"
        echo "Usage: $0 [default|http|production]"
        exit 1
        ;;
esac

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Stack is starting up!"
echo ""
echo "Access points:"
echo "- WordPress: http://localhost:8888"
echo "- WordPress Admin: http://localhost:8888/wp/wp-admin"

if [ "$MODE" = "http" ] || [ "$MODE" = "production" ]; then
    echo "- MCP Server Health: http://localhost:9001/health"
fi

echo ""
echo "View logs with: ./logs.sh"
echo "Stop services with: ./stop.sh"
echo ""
