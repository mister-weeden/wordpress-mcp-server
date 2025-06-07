FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# Install the package in development mode
RUN pip install -e .

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Create logs directory
RUN mkdir -p /app/logs

# Expose MCP server port (9000+ range)
EXPOSE 9001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:9001/health || exit 1

# Default environment variables
ENV WORDPRESS_URL=http://bedrock:8080
ENV WORDPRESS_USERNAME=admin
ENV WORDPRESS_PASSWORD=admin
ENV MCP_SERVER_PORT=9001
ENV MCP_SERVER_MODE=stdio
ENV LOG_LEVEL=INFO

# Default command - stdio mode for Claude Desktop
CMD ["wordpress-mcp-server", "--mode", "stdio"]

# Alternative commands can be specified:
# For HTTP mode: CMD ["wordpress-mcp-server", "--mode", "http", "--host", "0.0.0.0"]
# For testing: CMD ["wordpress-mcp-server", "--test-connection"]