#!/bin/bash

SERVICE=${1:-all}

echo "📋 Viewing logs for: $SERVICE"
echo "=========================="

case $SERVICE in
    "all")
        docker-compose logs -f --tail=50
        ;;
    "wordpress"|"wp"|"bedrock")
        docker-compose logs -f --tail=50 bedrock
        ;;
    "mcp"|"mcp-server")
        docker-compose logs -f --tail=50 wordpress-mcp-server
        ;;
    "db"|"database")
        docker-compose logs -f --tail=50 bedrock-db
        ;;
    "nginx")
        docker-compose logs -f --tail=50 nginx
        ;;
    *)
        echo "❌ Invalid service: $SERVICE"
        echo "Usage: $0 [all|wordpress|mcp|db|nginx]"
        exit 1
        ;;
esac
