"""
WordPress MCP Server - Command Line Interface
"""

import argparse
import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

from .server import WordPressMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="WordPress MCP Server - Enable Claude AI to manage WordPress blogs",
        epilog="""
Examples:
  %(prog)s --mode stdio                          # Run for Claude Desktop
  %(prog)s --mode http --mcp-port 9001          # Run HTTP server
  %(prog)s --wordpress-url http://localhost:8080 # Custom WordPress URL
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # WordPress configuration
    wp_group = parser.add_argument_group("WordPress Configuration")
    wp_group.add_argument(
        "--wordpress-url",
        default=os.getenv("WORDPRESS_URL", "http://192.168.0.10:8888"),
        help="WordPress site URL (default: %(default)s)",
    )
    wp_group.add_argument(
        "--username",
        default=os.getenv("WORDPRESS_USERNAME", "admin"),
        help="WordPress username (default: %(default)s)",
    )
    wp_group.add_argument(
        "--password",
        default=os.getenv("WORDPRESS_PASSWORD", "admin"),
        help="WordPress password (default: %(default)s)",
    )

    # MCP Server configuration
    mcp_group = parser.add_argument_group("MCP Server Configuration")
    mcp_group.add_argument(
        "--mcp-port",
        type=int,
        default=int(os.getenv("MCP_SERVER_PORT", "9001")),
        help="MCP server port (9000+ range recommended, default: %(default)s)",
    )
    mcp_group.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default=os.getenv("MCP_SERVER_MODE", "stdio"),
        help="Server transport mode (default: %(default)s)",
    )
    mcp_group.add_argument(
        "--host",
        default=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        help="Host to bind HTTP server to (only for http mode, default: %(default)s)",
    )

    # Logging configuration
    log_group = parser.add_argument_group("Logging Configuration")
    log_group.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=os.getenv("LOG_LEVEL", "INFO"),
        help="Set the logging level (default: %(default)s)",
    )
    log_group.add_argument(
        "--log-file",
        default=os.getenv("LOG_FILE"),
        help="Log to file instead of console",
    )

    # Utility arguments
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test WordPress connection and exit",
    )
    parser.add_argument("--config-file", help="Load configuration from file")

    return parser


def setup_logging(level: str, log_file: str = None):
    """Setup logging configuration"""
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    # Configure logging
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if log_file:
        logging.basicConfig(
            level=numeric_level, format=log_format, filename=log_file, filemode="a"
        )
        # Also log to console for important messages
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger("").addHandler(console)
    else:
        logging.basicConfig(level=numeric_level, format=log_format, stream=sys.stdout)


def validate_configuration(args):
    """Validate configuration arguments"""
    errors = []

    # Validate WordPress URL
    if not args.wordpress_url.startswith(("http://", "https://")):
        errors.append("WordPress URL must start with http:// or https://")

    # Validate port ranges
    if ":" in args.wordpress_url:
        try:
            wp_port = int(args.wordpress_url.split(":")[-1].split("/")[0])
            if wp_port < 8000 or wp_port >= 9000:
                logger.warning(
                    f"WordPress port {wp_port} is outside recommended 8000-8999 range"
                )
        except ValueError:
            pass  # URL might not have a port

    if args.mcp_port < 9000:
        logger.warning(f"MCP port {args.mcp_port} is below recommended 9000+ range")

    # Check for required credentials
    if not args.username or not args.password:
        errors.append("WordPress username and password are required")

    if errors:
        for error in errors:
            logger.error(error)
        sys.exit(1)


async def test_wordpress_connection(args):
    """Test WordPress connection and exit"""
    from .server import WordPressClient

    print(f"Testing WordPress connection to: {args.wordpress_url}")
    print(f"Username: {args.username}")
    print("-" * 50)

    try:
        async with WordPressClient(
            args.wordpress_url, args.username, args.password
        ) as wp_client:
            result = await wp_client.authenticate()

            if result["success"]:
                user = result["user"]
                print("✅ Connection successful!")
                print(f"   Connected as: {user.get('name', 'Unknown')}")
                print(f"   Username: {user.get('username', 'Unknown')}")
                print(f"   Email: {user.get('email', 'Unknown')}")
                print(f"   Roles: {', '.join(user.get('roles', []))}")
                sys.exit(0)
            else:
                print(f"❌ Connection failed: {result['error']}")
                sys.exit(1)

    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        sys.exit(1)


async def run_server(args):
    """Run the MCP server"""
    logger.info("Starting WordPress MCP Server")
    logger.info(f"WordPress URL: {args.wordpress_url}")
    logger.info(f"Mode: {args.mode}")
    logger.info(f"MCP Port: {args.mcp_port}")

    # Create server instance
    server = WordPressMCPServer(
        wordpress_url=args.wordpress_url,
        username=args.username,
        password=args.password,
        mcp_port=args.mcp_port,
    )

    try:
        if args.mode == "stdio":
            logger.info("Starting server in stdio mode (for Claude Desktop)")
            await server.run_stdio()
        elif args.mode == "http":
            logger.info(f"Starting server in HTTP mode on {args.host}:{args.mcp_port}")
            await server.run_http(host=args.host, port=args.mcp_port)
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


async def main_async():
    """Async main function"""
    # Load environment variables
    load_dotenv()

    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level, args.log_file)

    # Validate configuration
    validate_configuration(args)

    # Test connection if requested
    if args.test_connection:
        await test_wordpress_connection(args)
        return

    # Run the server
    await run_server(args)


def main():
    """Main entry point"""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
