"""MCP Hub Server — The App Store for MCP Servers."""

from mcp.server.fastmcp import FastMCP

from src.tools.hub import register_hub_tools

mcp = FastMCP(
    "MCP Hub",
    instructions=(
        "The App Store for MCP Servers. Search, discover and install "
        "MCP servers from one place. Browse 50+ servers across categories "
        "like Developer Tools, Finance, Science, Security and more. "
        "Get instant install configs for any server."
    ),
)

register_hub_tools(mcp)


def main():
    """Server starten."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
