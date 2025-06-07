#!/bin/bash

echo "⚠️  WARNING: This will destroy all data!"
echo "======================================="
echo ""
read -p "Are you sure you want to reset everything? (yes/no): " -r
echo ""

if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "🗑️  Stopping and removing all containers and volumes..."
    docker-compose down -v
    
    echo "🧹 Cleaning up Docker resources..."
    docker system prune -f
    
    echo "✅ Reset complete!"
    echo ""
    echo "To start fresh: ./setup.sh && ./start.sh"
else
    echo "❌ Reset cancelled."
fi
