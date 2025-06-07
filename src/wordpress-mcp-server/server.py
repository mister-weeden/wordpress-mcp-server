"""
WordPress MCP Server - Main server implementation
"""

import asyncio
import logging
import mcp
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urljoin
import aiohttp
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    Prompt,
    PromptMessage,
    PromptArgument,
)

# Configure logging
logger = logging.getLogger(__name__)


class WordPressClient:
    """WordPress REST API client"""

    def __init__(self, base_url: str, username: str = "admin", password: str = "admin"):
        self.base_url = base_url.rstrip("/")
        self.api_base = f"{self.base_url}/wp-json/wp/v2"
        self.username = username
        self.password = password
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def authenticate(self) -> Dict[str, Any]:
        """Test authentication with WordPress"""
        try:
            auth = aiohttp.BasicAuth(self.username, self.password)
            async with self.session.get(
                f"{self.api_base}/users/me", auth=auth
            ) as response:
                if response.status == 200:
                    user_data = await response.json()
                    return {"success": True, "user": user_data}
                else:
                    return {
                        "success": False,
                        "error": f"Authentication failed: {response.status}",
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        excerpt: str = "",
        categories: List[str] = None,
        tags: List[str] = None,
    ) -> Dict[str, Any]:
        """Create a new WordPress post"""
        try:
            auth = aiohttp.BasicAuth(self.username, self.password)

            # Prepare post data
            post_data = {
                "title": title,
                "content": content,
                "status": status,  # draft, publish, private
                "excerpt": excerpt,
                "format": "standard",
            }

            # Handle categories
            if categories:
                # First, get existing categories or create new ones
                category_ids = await self._get_or_create_categories(categories)
                post_data["categories"] = category_ids

            # Handle tags
            if tags:
                tag_ids = await self._get_or_create_tags(tags)
                post_data["tags"] = tag_ids

            async with self.session.post(
                f"{self.api_base}/posts",
                json=post_data,
                auth=auth,
                headers={"Content-Type": "application/json"},
            ) as response:
                if response.status == 201:
                    post = await response.json()
                    return {
                        "success": True,
                        "post": {
                            "id": post["id"],
                            "title": post["title"]["rendered"],
                            "url": post["link"],
                            "status": post["status"],
                            "date": post["date"],
                        },
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"Failed to create post: {response.status} - {error_text}",
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def update_post(
        self, post_id: int, title: str = None, content: str = None, status: str = None
    ) -> Dict[str, Any]:
        """Update an existing WordPress post"""
        try:
            auth = aiohttp.BasicAuth(self.username, self.password)

            post_data = {}
            if title:
                post_data["title"] = title
            if content:
                post_data["content"] = content
            if status:
                post_data["status"] = status

            async with self.session.post(
                f"{self.api_base}/posts/{post_id}",
                json=post_data,
                auth=auth,
                headers={"Content-Type": "application/json"},
            ) as response:
                if response.status == 200:
                    post = await response.json()
                    return {
                        "success": True,
                        "post": {
                            "id": post["id"],
                            "title": post["title"]["rendered"],
                            "url": post["link"],
                            "status": post["status"],
                        },
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"Failed to update post: {response.status} - {error_text}",
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def list_posts(
        self, status: str = "any", per_page: int = 10
    ) -> Dict[str, Any]:
        """List WordPress posts"""
        try:
            auth = aiohttp.BasicAuth(self.username, self.password)
            params = {
                "status": status,
                "per_page": per_page,
                "orderby": "date",
                "order": "desc",
            }

            async with self.session.get(
                f"{self.api_base}/posts", params=params, auth=auth
            ) as response:
                if response.status == 200:
                    posts = await response.json()
                    return {
                        "success": True,
                        "posts": [
                            {
                                "id": post["id"],
                                "title": post["title"]["rendered"],
                                "url": post["link"],
                                "status": post["status"],
                                "date": post["date"],
                                "excerpt": post["excerpt"]["rendered"],
                            }
                            for post in posts
                        ],
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to list posts: {response.status}",
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _get_or_create_categories(self, category_names: List[str]) -> List[int]:
        """Get category IDs or create categories if they don't exist"""
        category_ids = []
        auth = aiohttp.BasicAuth(self.username, self.password)

        for name in category_names:
            # First try to find existing category
            async with self.session.get(
                f"{self.api_base}/categories", params={"search": name}, auth=auth
            ) as response:
                if response.status == 200:
                    categories = await response.json()
                    existing = next(
                        (
                            cat
                            for cat in categories
                            if cat["name"].lower() == name.lower()
                        ),
                        None,
                    )

                    if existing:
                        category_ids.append(existing["id"])
                    else:
                        # Create new category
                        async with self.session.post(
                            f"{self.api_base}/categories",
                            json={"name": name},
                            auth=auth,
                        ) as create_response:
                            if create_response.status == 201:
                                new_category = await create_response.json()
                                category_ids.append(new_category["id"])

        return category_ids

    async def _get_or_create_tags(self, tag_names: List[str]) -> List[int]:
        """Get tag IDs or create tags if they don't exist"""
        tag_ids = []
        auth = aiohttp.BasicAuth(self.username, self.password)

        for name in tag_names:
            # First try to find existing tag
            async with self.session.get(
                f"{self.api_base}/tags", params={"search": name}, auth=auth
            ) as response:
                if response.status == 200:
                    tags = await response.json()
                    existing = next(
                        (tag for tag in tags if tag["name"].lower() == name.lower()),
                        None,
                    )

                    if existing:
                        tag_ids.append(existing["id"])
                    else:
                        # Create new tag
                        async with self.session.post(
                            f"{self.api_base}/tags", json={"name": name}, auth=auth
                        ) as create_response:
                            if create_response.status == 201:
                                new_tag = await create_response.json()
                                tag_ids.append(new_tag["id"])

        return tag_ids


class WordPressMCPServer:
    """MCP Server for WordPress blog management"""

    def __init__(
        self,
        wordpress_url: str,
        username: str = "admin",
        password: str = "admin",
        mcp_port: int = 9001,
    ):
        self.wordpress_url = wordpress_url
        self.username = username
        self.password = password
        self.mcp_port = mcp_port
        self.server = Server("wordpress-blog-server")
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP handlers"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available WordPress tools"""
            return [
                Tool(
                    name="create_blog_post",
                    description="Create a new blog post in WordPress",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the blog post",
                            },
                            "content": {
                                "type": "string",
                                "description": "The main content of the blog post (HTML or plain text)",
                            },
                            "status": {
                                "type": "string",
                                "enum": ["draft", "publish", "private"],
                                "description": "Post status",
                                "default": "draft",
                            },
                            "excerpt": {
                                "type": "string",
                                "description": "Short excerpt/summary of the post",
                                "default": "",
                            },
                            "categories": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of category names for the post",
                                "default": [],
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of tag names for the post",
                                "default": [],
                            },
                        },
                        "required": ["title", "content"],
                    },
                ),
                Tool(
                    name="update_blog_post",
                    description="Update an existing blog post in WordPress",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "post_id": {
                                "type": "integer",
                                "description": "The ID of the post to update",
                            },
                            "title": {
                                "type": "string",
                                "description": "New title for the post",
                            },
                            "content": {
                                "type": "string",
                                "description": "New content for the post",
                            },
                            "status": {
                                "type": "string",
                                "enum": ["draft", "publish", "private"],
                                "description": "New status for the post",
                            },
                        },
                        "required": ["post_id"],
                    },
                ),
                Tool(
                    name="list_blog_posts",
                    description="List existing blog posts from WordPress",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["draft", "publish", "private", "any"],
                                "description": "Filter posts by status",
                                "default": "any",
                            },
                            "per_page": {
                                "type": "integer",
                                "description": "Number of posts to retrieve",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 100,
                            },
                        },
                    },
                ),
                Tool(
                    name="test_wordpress_connection",
                    description="Test the connection to WordPress and verify authentication",
                    inputSchema={"type": "object", "properties": {}},
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
            """Handle tool calls"""

            if name == "create_blog_post":
                async with WordPressClient(
                    self.wordpress_url, self.username, self.password
                ) as wp_client:
                    result = await wp_client.create_post(
                        title=arguments["title"],
                        content=arguments["content"],
                        status=arguments.get("status", "draft"),
                        excerpt=arguments.get("excerpt", ""),
                        categories=arguments.get("categories", []),
                        tags=arguments.get("tags", []),
                    )

                    if result["success"]:
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=f"Successfully created blog post!\n\n"
                                    f"Title: {result['post']['title']}\n"
                                    f"ID: {result['post']['id']}\n"
                                    f"Status: {result['post']['status']}\n"
                                    f"URL: {result['post']['url']}\n"
                                    f"Date: {result['post']['date']}",
                                )
                            ]
                        )
                    else:
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=f"Failed to create blog post: {result['error']}",
                                )
                            ],
                            isError=True,
                        )

            elif name == "update_blog_post":
                async with WordPressClient(
                    self.wordpress_url, self.username, self.password
                ) as wp_client:
                    result = await wp_client.update_post(
                        post_id=arguments["post_id"],
                        title=arguments.get("title"),
                        content=arguments.get("content"),
                        status=arguments.get("status"),
                    )

                    if result["success"]:
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=f"Successfully updated blog post!\n\n"
                                    f"Title: {result['post']['title']}\n"
                                    f"ID: {result['post']['id']}\n"
                                    f"Status: {result['post']['status']}\n"
                                    f"URL: {result['post']['url']}",
                                )
                            ]
                        )
                    else:
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=f"Failed to update blog post: {result['error']}",
                                )
                            ],
                            isError=True,
                        )

            elif name == "list_blog_posts":
                async with WordPressClient(
                    self.wordpress_url, self.username, self.password
                ) as wp_client:
                    result = await wp_client.list_posts(
                        status=arguments.get("status", "any"),
                        per_page=arguments.get("per_page", 10),
                    )

                    if result["success"]:
                        posts_text = "Blog Posts:\n\n"
                        for post in result["posts"]:
                            posts_text += (
                                f"ID: {post['id']}\n"
                                f"Title: {post['title']}\n"
                                f"Status: {post['status']}\n"
                                f"Date: {post['date']}\n"
                                f"URL: {post['url']}\n"
                                f"Excerpt: {post['excerpt'][:100]}...\n\n"
                            )

                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=posts_text
                                    if result["posts"]
                                    else "No posts found.",
                                )
                            ]
                        )
                    else:
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=f"Failed to list posts: {result['error']}",
                                )
                            ],
                            isError=True,
                        )

            elif name == "test_wordpress_connection":
                async with WordPressClient(
                    self.wordpress_url, self.username, self.password
                ) as wp_client:
                    result = await wp_client.authenticate()

                    if result["success"]:
                        user = result["user"]
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=f"WordPress connection successful!\n\n"
                                    f"Connected as: {user.get('name', 'Unknown')}\n"
                                    f"Username: {user.get('username', 'Unknown')}\n"
                                    f"Email: {user.get('email', 'Unknown')}\n"
                                    f"Role: {', '.join(user.get('roles', []))}\n"
                                    f"Site URL: {self.wordpress_url}",
                                )
                            ]
                        )
                    else:
                        return CallToolResult(
                            content=[
                                TextContent(
                                    type="text",
                                    text=f"WordPress connection failed: {result['error']}",
                                )
                            ],
                            isError=True,
                        )

            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                    isError=True,
                )

        @self.server.list_prompts()
        async def handle_list_prompts() -> List[Prompt]:
            """List available prompts for blog writing"""
            return [
                Prompt(
                    name="thesis_blog_post",
                    description="Generate a blog post about Master's thesis research progress",
                    arguments=[
                        PromptArgument(
                            name="topic",
                            description="The specific research topic or milestone to write about",
                            required=True,
                        ),
                        PromptArgument(
                            name="findings",
                            description="Key findings, insights, or progress made",
                            required=False,
                        ),
                        PromptArgument(
                            name="challenges",
                            description="Challenges encountered and how they were addressed",
                            required=False,
                        ),
                    ],
                ),
                Prompt(
                    name="algorithm_analysis_post",
                    description="Generate a blog post about algorithm analysis and complexity",
                    arguments=[
                        PromptArgument(
                            name="algorithm",
                            description="The algorithm being analyzed",
                            required=True,
                        ),
                        PromptArgument(
                            name="complexity",
                            description="Time/space complexity analysis",
                            required=False,
                        ),
                        PromptArgument(
                            name="applications",
                            description="Real-world applications of the algorithm",
                            required=False,
                        ),
                    ],
                ),
            ]

        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: dict) -> GetPromptResult:
            """Handle prompt requests"""

            if name == "thesis_blog_post":
                topic = arguments.get("topic", "")
                findings = arguments.get("findings", "")
                challenges = arguments.get("challenges", "")

                prompt_text = f"""Write a detailed blog post about my Master's thesis research progress. Here are the details:

**Topic:** {topic}

**Key Findings/Progress:** {findings}

**Challenges Encountered:** {challenges}

Please structure the blog post with:
1. An engaging introduction
2. Clear explanation of the research topic
3. Discussion of methodology and approach
4. Key findings and insights
5. Challenges faced and solutions
6. Next steps and future work
7. Conclusion

The tone should be informative but accessible to both technical and non-technical readers. Include relevant technical details but explain them clearly."""

                return GetPromptResult(
                    description=f"Blog post template for thesis research on: {topic}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text),
                        )
                    ],
                )

            elif name == "algorithm_analysis_post":
                algorithm = arguments.get("algorithm", "")
                complexity = arguments.get("complexity", "")
                applications = arguments.get("applications", "")

                prompt_text = f"""Write a comprehensive blog post analyzing the following algorithm:

**Algorithm:** {algorithm}

**Complexity Analysis:** {complexity}

**Applications:** {applications}

Please structure the blog post with:
1. Introduction to the algorithm and its importance
2. Clear explanation of how the algorithm works
3. Step-by-step breakdown with examples
4. Time and space complexity analysis
5. Comparison with alternative approaches
6. Real-world applications and use cases
7. Implementation considerations
8. Conclusion

Make sure to explain mathematical concepts clearly and include practical examples. The post should be educational and help readers understand both the theory and practical aspects of the algorithm."""

                return GetPromptResult(
                    description=f"Blog post template for algorithm analysis: {algorithm}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text),
                        )
                    ],
                )

            else:
                raise ValueError(f"Unknown prompt: {name}")

    async def run_stdio(self):
        """Run server with stdio transport (for Claude Desktop)"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="wordpress-blog-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None, experimental_capabilities=None
                    ),
                ),
            )

    async def run_http(self, host: str = "0.0.0.0", port: int = None):
        """Run server with HTTP transport (for remote access)"""
        if port is None:
            port = self.mcp_port

        from aiohttp import web

        app = web.Application()

        async def health_check(request):
            return web.json_response({"status": "healthy", "server": "wordpress-mcp"})

        async def mcp_capabilities(request):
            capabilities = self.server.get_capabilities(
                notification_options=None, experimental_capabilities=None
            )
            return web.json_response(
                {
                    "capabilities": capabilities,
                    "server_info": {
                        "name": "wordpress-blog-server",
                        "version": "1.0.0",
                    },
                }
            )

        app.router.add_get("/health", health_check)
        app.router.add_get("/capabilities", mcp_capabilities)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

        logger.info(f"HTTP MCP server running on http://{host}:{port}")
        logger.info(f"Health check: http://{host}:{port}/health")
        logger.info(f"Capabilities: http://{host}:{port}/capabilities")

        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            logger.info("Shutting down HTTP server...")
        finally:
            await runner.cleanup()
