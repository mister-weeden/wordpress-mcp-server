# WordPress MCP Server - Port Configuration Guide

## 🚪 Port Layout Overview

The system uses a clear port separation strategy:

| Service        | Port Range | Default Port | Purpose                    |
| -------------- | ---------- | ------------ | -------------------------- |
| **WordPress**  | 8000-8999  | **8888**     | WordPress web interface    |
| **MCP Server** | 9000+      | **9001**     | MCP protocol communication |

## ⚙️ Configuration Examples

### Standard Setup (Recommended)

```bash
# WordPress runs on port 8888
# MCP Server runs on port 9001

# Start MCP server for Claude Desktop (stdio mode)
python wordpress_mcp_server.py \
  --wordpress-url http://192.168.0.10:8888 \
  --mcp-port 9001 \
  --mode stdio

# Or start MCP server for remote access (HTTP mode)
python wordpress_mcp_server.py \
  --wordpress-url http://192.168.0.10:8888 \
  --mcp-port 9001 \
  --mode http \
  --host 0.0.0.0
```

### Environment Variables

```bash
# .env file configuration
WORDPRESS_URL=http://192.168.0.10:8888
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=admin
MCP_SERVER_PORT=9001
MCP_SERVER_MODE=stdio
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "wordpress-blog": {
      "command": "python",
      "args": [
        "/path/to/wordpress_mcp_server.py",
        "--wordpress-url",
        "http://192.168.0.10:8888",
        "--mcp-port",
        "9001",
        "--mode",
        "stdio"
      ],
      "env": {
        "WORDPRESS_URL": "http://192.168.0.10:8888",
        "WORDPRESS_USERNAME": "admin",
        "WORDPRESS_PASSWORD": "admin"
      }
    }
  }
}
```

## 🐳 Docker Configuration

### docker-compose.yml

```yaml
version: "3.8"

services:
  # Default stdio mode for Claude Desktop
  wordpress-mcp-server:
    build: .
    container_name: wordpress-mcp-server
    environment:
      - WORDPRESS_URL=http://192.168.0.10:8888
      - WORDPRESS_USERNAME=admin
      - WORDPRESS_PASSWORD=admin
    command: >
      python wordpress_mcp_server.py 
      --wordpress-url http://192.168.0.10:8888
      --mcp-port 9001
      --mode stdio

  # Optional HTTP mode for remote access
  wordpress-mcp-server-http:
    build: .
    container_name: wordpress-mcp-server-http
    ports:
      - "9001:9001" # MCP server on port 9001
    environment:
      - WORDPRESS_URL=http://192.168.0.10:8888
      - WORDPRESS_USERNAME=admin
      - WORDPRESS_PASSWORD=admin
    command: >
      python wordpress_mcp_server.py 
      --wordpress-url http://192.168.0.10:8888
      --mcp-port 9001
      --mode http
      --host 0.0.0.0
    profiles:
      - http
```

### Running Docker Services

```bash
# Start stdio mode (for Claude Desktop)
docker-compose up -d wordpress-mcp-server

# Start HTTP mode (for remote access)
docker-compose --profile http up -d wordpress-mcp-server-http
```

## 🔍 Testing Port Configuration

### Test WordPress Connection (Port 8888)

```bash
# Test WordPress web interface
curl http://192.168.0.10:8888

# Test WordPress REST API
curl http://192.168.0.10:8888/wp-json/wp/v2/
```

### Test MCP Server (Port 9001)

```bash
# For HTTP mode only
curl http://localhost:9001/health
curl http://localhost:9001/capabilities

# For stdio mode - use the test script
python test_wordpress.py
```

## 🛠️ Troubleshooting Port Issues

### Port Conflicts

```bash
# Check if ports are in use
netstat -an | grep :8888
netstat -an | grep :9001

# Or with lsof
lsof -i :8888
lsof -i :9001
```

### Firewall Configuration

```bash
# Allow WordPress port (if needed)
sudo ufw allow 8888

# Allow MCP server port (only for HTTP mode)
sudo ufw allow 9001
```

### Changing Ports

If you need to use different ports:

```bash
# Example: WordPress on 8080, MCP on 9002
python wordpress_mcp_server.py \
  --wordpress-url http://192.168.0.10:8080 \
  --mcp-port 9002 \
  --mode stdio
```

Update your WordPress container:

```bash
docker run -p 8080:80 wordpress
```

## 🔒 Security Considerations

### Port Access Rules

- **Port 8888** (WordPress): Should be accessible from your local network
- **Port 9001** (MCP Server):
  - **stdio mode**: No network port needed (communication via stdin/stdout)
  - **HTTP mode**: Only accessible from trusted networks/localhost

### Recommended Network Setup

```bash
# WordPress: Local network access
iptables -A INPUT -p tcp --dport 8888 -s 192.168.0.0/24 -j ACCEPT

# MCP Server HTTP mode: Localhost only (most secure)
iptables -A INPUT -p tcp --dport 9001 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 9001 -j DROP
```

## 📋 Quick Reference Commands

### Start Services

```bash
# Start WordPress (if using Docker)
docker run -d -p 8888:80 --name wordpress wordpress

# Start MCP Server (stdio mode for Claude Desktop)
python wordpress_mcp_server.py --mode stdio

# Start MCP Server (HTTP mode for remote access)
python wordpress_mcp_server.py --mode http --mcp-port 9001
```

### Check Status

```bash
# WordPress health
curl -I http://192.168.0.10:8888

# MCP Server health (HTTP mode only)
curl http://localhost:9001/health

# Test full integration
python test_wordpress.py
```

This port configuration ensures clean separation between your WordPress installation and the MCP server, avoiding conflicts while maintaining security best practices.
