"""Hub-Tools — MCP-Server suchen, entdecken und installieren."""

import json
from mcp.server.fastmcp import FastMCP

from src.catalog import get_connection


def register_hub_tools(mcp: FastMCP):
    """Hub-Tools registrieren."""

    @mcp.tool()
    async def search_servers(query: str) -> dict:
        """Search for MCP servers by keyword, category, or capability.

        Find the perfect MCP server for any task. Searches across
        names, descriptions, categories and tags.

        Args:
            query: Search term (e.g. "weather", "database", "crypto", "payments")
        """
        conn = get_connection()
        query_lower = f"%{query.lower()}%"

        rows = conn.execute("""
            SELECT * FROM servers
            WHERE LOWER(name) LIKE ?
               OR LOWER(description) LIKE ?
               OR LOWER(category) LIKE ?
               OR LOWER(tags) LIKE ?
            ORDER BY name
            LIMIT 20
        """, (query_lower, query_lower, query_lower, query_lower)).fetchall()

        results = []
        for r in rows:
            results.append({
                "id": r["id"],
                "name": r["name"],
                "description": r["description"],
                "category": r["category"],
                "author": r["author"],
                "requires_api_key": bool(r["requires_api_key"]),
                "free_tier": bool(r["free_tier"]),
                "github_url": r["github_url"],
            })

        return {
            "query": query,
            "results_count": len(results),
            "servers": results,
        }

    @mcp.tool()
    async def get_server_details(server_id: str) -> dict:
        """Get full details and install instructions for a specific MCP server.

        Returns everything needed to install and use the server,
        including the exact config to add to your MCP client.

        Args:
            server_id: Server ID (e.g. "solana-mcp-server", "mcp-server-github")
        """
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM servers WHERE id = ?", (server_id,)
        ).fetchone()

        if not row:
            return {"error": f"Server '{server_id}' not found"}

        install_args = json.loads(row["install_args"])
        tags = json.loads(row["tags"])

        # MCP-Config generieren
        short_name = server_id.replace("mcp-server-", "").replace("-mcp-server", "")
        mcp_config = {
            "mcpServers": {
                short_name: {
                    "command": row["install_command"],
                    "args": install_args,
                }
            }
        }

        return {
            "id": row["id"],
            "name": row["name"],
            "description": row["description"],
            "category": row["category"],
            "author": row["author"],
            "tags": tags,
            "requires_api_key": bool(row["requires_api_key"]),
            "free_tier": bool(row["free_tier"]),
            "github_url": row["github_url"],
            "pypi_url": row["pypi_url"],
            "install_config": mcp_config,
            "install_config_json": json.dumps(mcp_config, indent=2),
        }

    @mcp.tool()
    async def list_categories() -> dict:
        """List all available MCP server categories with server counts.

        Browse servers by category to discover new capabilities.
        """
        conn = get_connection()
        rows = conn.execute("""
            SELECT category, COUNT(*) as count
            FROM servers
            GROUP BY category
            ORDER BY count DESC
        """).fetchall()

        categories = []
        total = 0
        for r in rows:
            categories.append({
                "category": r["category"],
                "server_count": r["count"],
            })
            total += r["count"]

        return {
            "total_servers": total,
            "categories": categories,
        }

    @mcp.tool()
    async def list_servers(category: str = "", limit: int = 20) -> dict:
        """List MCP servers, optionally filtered by category.

        Browse the full catalog or filter by category to discover servers.

        Args:
            category: Filter by category (optional, e.g. "Developer Tools")
            limit: Maximum results (default: 20)
        """
        conn = get_connection()

        if category:
            rows = conn.execute("""
                SELECT * FROM servers
                WHERE LOWER(category) LIKE ?
                ORDER BY name
                LIMIT ?
            """, (f"%{category.lower()}%", limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM servers ORDER BY name LIMIT ?
            """, (limit,)).fetchall()

        servers = []
        for r in rows:
            servers.append({
                "id": r["id"],
                "name": r["name"],
                "description": r["description"],
                "category": r["category"],
                "author": r["author"],
                "free_tier": bool(r["free_tier"]),
            })

        return {
            "category_filter": category or "all",
            "results_count": len(servers),
            "servers": servers,
        }

    @mcp.tool()
    async def submit_server(
        server_id: str,
        name: str,
        description: str,
        category: str,
        github_url: str,
        install_command: str = "uvx",
        install_args: str = "[]",
        author: str = "",
    ) -> dict:
        """Submit a new MCP server to the Hub catalog.

        Add your own or a third-party MCP server so others can discover it.
        Submissions are stored locally and persist between sessions.

        Args:
            server_id: Unique ID (e.g. "my-cool-server")
            name: Display name (e.g. "My Cool MCP Server")
            description: What the server does (1-2 sentences)
            category: Category (e.g. "Developer Tools", "Finance", "Science")
            github_url: GitHub repository URL
            install_command: Install command ("uvx" or "npx")
            install_args: Install args as JSON array (e.g. '["my-cool-server"]')
            author: Author name
        """
        from datetime import datetime

        conn = get_connection()

        # Prüfen ob ID schon existiert
        existing = conn.execute(
            "SELECT id FROM servers WHERE id = ?", (server_id,)
        ).fetchone()
        if existing:
            return {"error": f"Server '{server_id}' already exists"}

        conn.execute("""
            INSERT INTO servers
            (id, name, description, category, install_command, install_args,
             github_url, author, tags, added_at, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '[]', ?, 'community')
        """, (server_id, name, description, category, install_command,
              install_args, github_url, author, datetime.utcnow().isoformat()))
        conn.commit()

        return {
            "status": "submitted",
            "server_id": server_id,
            "message": f"'{name}' has been added to the Hub catalog.",
        }

    @mcp.tool()
    async def get_install_config(server_id: str) -> dict:
        """Get the exact JSON config to install an MCP server.

        Copy-paste this into your .mcp.json or Claude Code settings
        to install the server immediately.

        Args:
            server_id: Server ID (e.g. "solana-mcp-server")
        """
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM servers WHERE id = ?", (server_id,)
        ).fetchone()

        if not row:
            return {"error": f"Server '{server_id}' not found"}

        install_args = json.loads(row["install_args"])
        short_name = server_id.replace("mcp-server-", "").replace("-mcp-server", "")

        config = {
            "mcpServers": {
                short_name: {
                    "command": row["install_command"],
                    "args": install_args,
                }
            }
        }

        return {
            "server": row["name"],
            "config_json": json.dumps(config, indent=2),
            "instructions": f"Add this to your .mcp.json or MCP client config to use {row['name']}.",
            "requires_api_key": bool(row["requires_api_key"]),
        }
