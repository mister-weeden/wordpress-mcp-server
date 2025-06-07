"""
WordPress MCP Server

A Model Context Protocol (MCP) server that enables Claude AI to create and manage WordPress blog posts.
Perfect for documenting research, thesis work, and technical projects.
"""

__version__ = "1.0.0"
__author__ = "WordPress MCP Contributors"
__email__ = "contact@example.com"
__license__ = "MIT"

from .server import WordPressMCPServer, WordPressClient
from .cli import main as cli_main

__all__ = ["WordPressMCPServer", "WordPressClient", "cli_main", "__version__"]

# Package metadata
PACKAGE_NAME = "wordpress-mcp-server"
DESCRIPTION = (
    "A Model Context Protocol (MCP) server for WordPress blog management with Claude AI"
)
HOMEPAGE = "https://github.com/yourusername/wordpress-mcp-server"
