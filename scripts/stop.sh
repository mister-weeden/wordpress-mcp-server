#!/bin/bash

echo "🛑 Stopping WordPress MCP Server Stack"
echo "====================================="

# Stop all services
docker-compose down

echo "✅ All services stopped."
echo ""
echo "To start again: ./start.sh"
echo "To remove all data: ./reset.sh"
echo ""
