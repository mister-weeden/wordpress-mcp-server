# WordPress MCP Server

[![PyPI version](https://badge.fury.io/py/wordpress-mcp-server.svg)](https://badge.fury.io/py/wordpress-mcp-server)
[![Python versions](https://img.shields.io/pypi/pyversions/wordpress-mcp-server.svg)](https://pypi.org/project/wordpress-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server that enables Claude AI to create and manage WordPress blog posts. Perfect for researchers, students, and professionals who want to document their work, share insights, and build a technical blog with AI assistance.

## 🚀 Features

- **Direct WordPress Integration**: Create, update, and manage blog posts through Claude
- **Academic Focus**: Built-in prompts for thesis documentation and research blogging
- **Flexible Deployment**: Support for both Claude Desktop (stdio) and remote (HTTP) modes
- **Rich Content Support**: Handle categories, tags, excerpts, and full HTML content
- **Port-Aware Configuration**: Clean separation between WordPress (8000+) and MCP (9000+) ports
- **Type Safety**: Full type hints and async/await support

## 📦 Installation

```bash
pip install wordpress-mcp-server
```

## 🎯 Quick Start

### 1. Install and Configure

```bash
# Install the package
pip install wordpress-mcp-server

# Test connection to your WordPress site
wordpress-mcp-server --test-connection --wordpress-url http://your-site.com
```

### 2. Claude Desktop Integration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "wordpress-blog": {
      "command": "wordpress-mcp-server",
      "args": ["--mode", "stdio"],
      "env": {
        "WORDPRESS_URL": "http://your-wordpress-site.com",
        "WORDPRESS_USERNAME": "your-username",
        "WORDPRESS_PASSWORD": "your-password"
      }
    }
  }
}
```

### 3. Start Blogging with Claude

Once configured, you can ask Claude to:

```
"Create a blog post about my research on Fast Fourier Transform algorithms"

"Write a thesis update documenting my progress with divide-and-conquer algorithms"

"List my recent blog posts and their status"

"Update post ID 15 with new findings from my experiments"
```

## 🔧 Configuration Options

### Environment Variables

```bash
export WORDPRESS_URL="http://your-site.com"
export WORDPRESS_USERNAME="admin"
export WORDPRESS_PASSWORD="your-password"
export MCP_SERVER_PORT="9001"
export MCP_SERVER_MODE="stdio"
```

### Command Line Options

```bash
# Basic usage
wordpress-mcp-server --mode stdio

# Custom WordPress URL and port
wordpress-mcp-server \
  --wordpress-url http://localhost:8888 \
  --mcp-port 9001 \
  --mode stdio

# HTTP mode for remote access
wordpress-mcp-server \
  --mode http \
  --host 0.0.0.0 \
  --mcp-port 9001

# Test connection
wordpress-mcp-server --test-connection
```

## 🎓 Perfect for Academic Blogging

### Built-in Academic Prompts

The server includes specialized prompts for academic and research blogging:

#### Thesis Documentation

```
"Use the thesis_blog_post prompt to document my progress with:
- Topic: Machine Learning Algorithm Optimization
- Findings: Achieved 15% speed improvement with new caching strategy
- Challenges: Memory management issues with large datasets"
```

#### Algorithm Analysis

```
"Use the algorithm_analysis_post prompt for:
- Algorithm: Quicksort with median-of-three pivot selection
- Complexity: O(n log n) average case, O(n²) worst case
- Applications: Database indexing and real-time sorting systems"
```

### Recommended Blog Structure

- **Weekly Progress Updates**: Document research milestones and discoveries
- **Technical Deep Dives**: Explain complex algorithms and implementations
- **Problem-Solving Sessions**: Share debugging experiences and solutions
- **Literature Reviews**: Summarize and analyze research papers
- **Code Showcases**: Highlight implementations and optimizations

## 🛠️ Advanced Usage

### Docker Deployment

```bash
# Clone and setup
git clone https://github.com/your-repo/wordpress-mcp-server
cd wordpress-mcp-server

# Build and run with Docker Compose
docker-compose up -d

# Or with custom configuration
docker run -e WORDPRESS_URL=http://your-site.com \
           -e WORDPRESS_USERNAME=admin \
           -e WORDPRESS_PASSWORD=secret \
           wordpress-mcp-server
```

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-repo/wordpress-mcp-server
cd wordpress-mcp-server

# Setup development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]

# Run tests
pytest

# Run with development settings
wordpress-mcp-server --log-level DEBUG --test-connection
```

## 🔌 Available Tools

### Blog Management Tools

| Tool                        | Description                   | Parameters                                        |
| --------------------------- | ----------------------------- | ------------------------------------------------- |
| `create_blog_post`          | Create new blog post          | title, content, status, excerpt, categories, tags |
| `update_blog_post`          | Update existing post          | post_id, title, content, status                   |
| `list_blog_posts`           | List published/draft posts    | status, per_page                                  |
| `test_wordpress_connection` | Verify WordPress connectivity | none                                              |

### Example Tool Usage

```python
# Through Claude, you can:
"Create a blog post titled 'Understanding Big-O Notation' with content explaining
time complexity, add it to the 'Algorithms' category and tag it with 'computer-science',
'complexity-analysis', and 'education'"

"List my last 5 published posts to see what I've written recently"

"Update post ID 23 to change the status from draft to published"
```

## 🔒 Security Considerations

- **WordPress Credentials**: Use WordPress Application Passwords instead of admin passwords
- **Network Access**: Restrict MCP server access to trusted networks only
- **HTTPS**: Use HTTPS for WordPress URLs in production
- **Firewall Rules**: Configure appropriate firewall rules for port access

## 🐛 Troubleshooting

### Common Issues

1. **Connection Failed**

   ```bash
   # Test WordPress connection
   wordpress-mcp-server --test-connection

   # Check WordPress REST API
   curl http://your-site.com/wp-json/wp/v2/
   ```

2. **Port Conflicts**

   ```bash
   # Check port usage
   netstat -an | grep :9001

   # Use different port
   wordpress-mcp-server --mcp-port 9002
   ```

3. **Permission Errors**
   - Ensure WordPress user has post creation permissions
   - Check WordPress REST API is enabled
   - Verify user roles and capabilities

### Debug Mode

```bash
# Enable debug logging
wordpress-mcp-server --log-level DEBUG

# Log to file
wordpress-mcp-server --log-file wordpress-mcp.log
```

## 📋 Port Configuration

| Service    | Port Range | Default | Purpose       |
| ---------- | ---------- | ------- | ------------- |
| WordPress  | 8000-8999  | 8888    | Web interface |
| MCP Server | 9000+      | 9001    | MCP protocol  |

This separation ensures clean network architecture and avoids port conflicts.

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Run tests: `pytest`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Use Cases

### For Students

- Document thesis research progress
- Create technical tutorials and explanations
- Share project updates and insights
- Build a professional portfolio

### For Researchers

- Publish research findings and methodologies
- Create accessible explanations of complex topics
- Document experimental results
- Share literature reviews and analysis

### For Developers

- Write technical blog posts about algorithms
- Document software development processes
- Share coding insights and best practices
- Create educational programming content

## 📚 Examples

Check out our [examples directory](examples/) for:

- Sample Claude conversations
- Blog post templates
- Configuration examples
- Integration patterns

## 🔗 Links

- [PyPI Package](https://pypi.org/project/wordpress-mcp-server/)
- [GitHub Repository](https://github.com/your-repo/wordpress-mcp-server)
- [Documentation](https://github.com/your-repo/wordpress-mcp-server/wiki)
- [Issue Tracker](https://github.com/your-repo/wordpress-mcp-server/issues)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Made with ❤️ for the research and development community**

Transform your research journey into engaging blog content with the power of AI assistance!

# WordPress MCP Server - Complete Package Structure

## 📁 Directory Layout

```
wordpress-mcp-server/
├── 📁 src/
│   └── 📁 wordpress_mcp_server/
│       ├── 📄 __init__.py                 # Package initialization and metadata
│       ├── 📄 server.py                   # Main MCP server implementation
│       ├── 📄 cli.py                      # Command-line interface
│       └── 📄 py.typed                    # Type hints marker file
├── 📁 tests/
│   ├── 📄 __init__.py
│   ├── 📄 test_server.py                  # Server tests
│   ├── 📄 test_cli.py                     # CLI tests
│   └── 📄 conftest.py                     # Pytest configuration
├── 📁 examples/
│   ├── 📄 basic_usage.py                  # Usage examples
│   ├── 📄 claude_conversations.md         # Example conversations
│   └── 📁 docker_example/
│       ├── 📄 docker-compose.yml
│       └── 📄 .env.example
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 publish.yml                 # GitHub Actions CI/CD
├── 📄 pyproject.toml                      # Modern Python packaging config
├── 📄 setup.cfg                           # Additional build configuration
├── 📄 MANIFEST.in                         # File inclusion rules
├── 📄 README.md                           # Package documentation
├── 📄 LICENSE                             # MIT license
├── 📄 CHANGELOG.md                        # Version history
├── 📄 CONTRIBUTING.md                     # Contribution guidelines
├── 📄 Dockerfile                          # Docker container build
├── 📄 docker-compose.yml                  # Docker Compose setup
├── 📄 .gitignore                          # Git ignore rules
├── 📄 .dockerignore                       # Docker ignore rules
└── 📄 requirements.txt                    # Legacy requirements (optional)
```

## 🗂️ File Descriptions

### Core Package Files

| File                                   | Purpose             | Contains                       |
| -------------------------------------- | ------------------- | ------------------------------ |
| `src/wordpress_mcp_server/__init__.py` | Package entry point | Version, exports, metadata     |
| `src/wordpress_mcp_server/server.py`   | Main functionality  | MCP server, WordPress client   |
| `src/wordpress_mcp_server/cli.py`      | Command interface   | Argument parsing, entry points |
| `src/wordpress_mcp_server/py.typed`    | Type safety         | PEP 561 marker for type hints  |

### Configuration Files

| File             | Purpose           | Configures                        |
| ---------------- | ----------------- | --------------------------------- |
| `pyproject.toml` | Package metadata  | Dependencies, build system, tools |
| `setup.cfg`      | Additional config | Linting rules, test options       |
| `MANIFEST.in`    | File inclusion    | What files to include in package  |

### Documentation

| File              | Purpose            | Audience           |
| ----------------- | ------------------ | ------------------ |
| `README.md`       | Main documentation | Users, PyPI page   |
| `CHANGELOG.md`    | Version history    | Users, maintainers |
| `CONTRIBUTING.md` | Development guide  | Contributors       |
| `LICENSE`         | Legal terms        | Everyone           |

### Testing & CI/CD

| File                            | Purpose    | Used For          |
| ------------------------------- | ---------- | ----------------- |
| `tests/`                        | Test suite | Quality assurance |
| `.github/workflows/publish.yml` | Automation | CI/CD pipeline    |

### Deployment

| File                 | Purpose               | Deployment            |
| -------------------- | --------------------- | --------------------- |
| `Dockerfile`         | Container build       | Docker deployment     |
| `docker-compose.yml` | Service orchestration | Multi-container setup |

## 📦 Installation Methods

### 1. From PyPI (Production)

```bash
pip install wordpress-mcp-server
```

### 2. From Source (Development)

```bash
git clone https://github.com/YOUR_USERNAME/wordpress-mcp-server.git
cd wordpress-mcp-server
pip install -e .[dev]
```

### 3. From Docker

```bash
docker pull wordpress-mcp-server:latest
docker run -e WORDPRESS_URL=http://your-site.com wordpress-mcp-server
```

## 🚀 Quick Start Commands

### Package Usage

```bash
# Basic usage
wordpress-mcp-server --mode stdio

# With custom configuration
wordpress-mcp-server \
  --wordpress-url http://localhost:8888 \
  --mcp-port 9001 \
  --mode stdio

# Test connection
wordpress-mcp-server --test-connection

# HTTP mode for remote access
wordpress-mcp-server --mode http --host 0.0.0.0 --mcp-port 9001
```

### Development Commands

```bash
# Setup development environment
python -m venv venv
source venv/bin/activate
pip install -e .[dev,test]

# Run tests
pytest tests/ -v

# Lint code
black src tests
flake8 src tests
mypy src

# Build package
python -m build

# Check package
twine check dist/*
```

## 🔄 Workflow Overview

### Development Workflow

1. **Clone repository**
2. **Setup environment** (`venv`, install dependencies)
3. **Make changes** (code, tests, docs)
4. **Test locally** (pytest, linting)
5. **Commit and push**
6. **Create pull request**

### Release Workflow

1. **Update version** (pyproject.toml, **init**.py)
2. **Update CHANGELOG.md**
3. **Test thoroughly**
4. **Create GitHub release**
5. **GitHub Actions publishes to PyPI**

### User Workflow

1. **Install package** (`pip install wordpress-mcp-server`)
2. **Configure WordPress** (URL, credentials)
3. **Setup Claude Desktop** (config file)
4. **Start blogging** with AI assistance!

## 📋 File Creation Checklist

When setting up the package, create files in this order:

### Phase 1: Core Package

- [ ] `src/wordpress_mcp_server/__init__.py`
- [ ] `src/wordpress_mcp_server/server.py`
- [ ] `src/wordpress_mcp_server/cli.py`
- [ ] `src/wordpress_mcp_server/py.typed`

### Phase 2: Configuration

- [ ] `pyproject.toml`
- [ ] `MANIFEST.in`
- [ ] `setup.cfg` (optional)

### Phase 3: Documentation

- [ ] `README.md`
- [ ] `LICENSE`
- [ ] `CHANGELOG.md`
- [ ] `CONTRIBUTING.md`

### Phase 4: Testing

- [ ] `tests/__init__.py`
- [ ] `tests/test_server.py`
- [ ] `tests/test_cli.py`
- [ ] `tests/conftest.py`

### Phase 5: CI/CD

- [ ] `.github/workflows/publish.yml`
- [ ] `.gitignore`

### Phase 6: Docker (Optional)

- [ ] `Dockerfile`
- [ ] `docker-compose.yml`
- [ ] `.dockerignore`

### Phase 7: Examples

- [ ] `examples/basic_usage.py`
- [ ] `examples/claude_conversations.md`

## 🎯 Key Features

### For Users

- **Easy Installation**: `pip install wordpress-mcp-server`
- **Simple Configuration**: Environment variables and CLI options
- **Claude Integration**: Works seamlessly with Claude Desktop
- **Academic Focus**: Built-in prompts for research documentation

### For Developers

- **Modern Python**: Type hints, async/await, Python 3.8+
- **Quality Assurance**: Tests, linting, CI/CD
- **Documentation**: Comprehensive README and examples
- **Easy Contributing**: Clear development setup

### For Deployment

- **Multiple Options**: pip, Docker, source installation
- **Flexible Configuration**: CLI, environment variables, config files
- **Port Management**: Smart port allocation (8000+ for WordPress, 9000+ for MCP)

## 🌟 Next Steps

Once you've created this structure:

1. **Test locally** to ensure everything works
2. **Publish to Test PyPI** first for validation
3. **Create GitHub repository** and push code
4. **Setup GitHub Actions** for automated publishing
5. **Publish to PyPI** for worldwide access
6. **Share with community** and gather feedback

This package structure follows Python packaging best practices and will provide a professional, maintainable foundation for the WordPress MCP Server!
