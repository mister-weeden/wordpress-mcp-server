# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-06-06

### Added

- Initial release of WordPress MCP Server
- Core MCP server implementation with WordPress REST API integration
- Support for creating, updating, and listing blog posts
- Built-in prompts for academic and research blogging
- Support for both stdio (Claude Desktop) and HTTP (remote) transport modes
- Comprehensive CLI with configuration options
- Port-aware configuration (WordPress: 8000+, MCP: 9000+)
- WordPress authentication and connection testing
- Support for post categories and tags
- Docker deployment support
- Type hints and async/await throughout
- Comprehensive documentation and examples

### Features

- **Blog Management Tools**:
  - `create_blog_post`: Create new posts with rich metadata
  - `update_blog_post`: Update existing posts
  - `list_blog_posts`: Browse published and draft content
  - `test_wordpress_connection`: Verify connectivity
- **Academic Prompts**:
  - `thesis_blog_post`: Structured thesis documentation
  - `algorithm_analysis_post`: Technical algorithm explanations
- **Deployment Options**:
  - Claude Desktop integration (stdio mode)
  - Remote server deployment (HTTP mode)
  - Docker and Docker Compose support
- **Security Features**:
  - Environment variable configuration
  - WordPress Application Password support
  - Configurable host binding and port ranges

### Technical Details

- Python 3.8+ support
- Async/await architecture
- Full type annotations
- Comprehensive error handling
- Structured logging
- Configuration validation
- Health checks and monitoring endpoints

### Documentation

- Complete README with examples
- API documentation
- Configuration guides
- Troubleshooting section
- Contributing guidelines
- Docker deployment guide

[Unreleased]: https://github.com/yourusername/wordpress-mcp-server/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/wordpress-mcp-server/releases/tag/v1.0.0
