#!/bin/bash
set -e

echo "🚀 WordPress MCP Server - Docker Setup"
echo "====================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please review and update the values."
else
    echo "✅ .env file already exists."
fi

# Generate WordPress salts if not already set
if grep -q "generate-your-unique" .env; then
    echo "🔐 Generating WordPress security keys..."
    
    # Generate random keys (simplified version)
    AUTH_KEY=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    SECURE_AUTH_KEY=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    LOGGED_IN_KEY=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    NONCE_KEY=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    AUTH_SALT=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    SECURE_AUTH_SALT=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    LOGGED_IN_SALT=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    NONCE_SALT=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-64)
    
    # Update .env file
    sed -i "s/AUTH_KEY='generate-your-unique-auth-key-here'/AUTH_KEY='$AUTH_KEY'/" .env
    sed -i "s/SECURE_AUTH_KEY='generate-your-unique-secure-auth-key-here'/SECURE_AUTH_KEY='$SECURE_AUTH_KEY'/" .env
    sed -i "s/LOGGED_IN_KEY='generate-your-unique-logged-in-key-here'/LOGGED_IN_KEY='$LOGGED_IN_KEY'/" .env
    sed -i "s/NONCE_KEY='generate-your-unique-nonce-key-here'/NONCE_KEY='$NONCE_KEY'/" .env
    sed -i "s/AUTH_SALT='generate-your-unique-auth-salt-here'/AUTH_SALT='$AUTH_SALT'/" .env
    sed -i "s/SECURE_AUTH_SALT='generate-your-unique-secure-auth-salt-here'/SECURE_AUTH_SALT='$SECURE_AUTH_SALT'/" .env
    sed -i "s/LOGGED_IN_SALT='generate-your-unique-logged-in-salt-here'/LOGGED_IN_SALT='$LOGGED_IN_SALT'/" .env
    sed -i "s/NONCE_SALT='generate-your-unique-nonce-salt-here'/NONCE_SALT='$NONCE_SALT'/" .env
    
    echo "✅ Generated unique WordPress security keys."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs nginx/ssl scripts

# Pull Docker images
echo "📦 Pulling Docker images..."
docker-compose pull

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review .env file and update any values as needed"
echo "2. Run: ./start.sh to start the services"
echo "3. Access WordPress at: http://localhost:8888"
echo "4. Configure Claude Desktop with the MCP server"
echo ""
