# MCP Hub 🏪

**The App Store for MCP Servers** — discover, search and install MCP servers from one place.

Instead of manually searching GitHub and configuring each server, use MCP Hub to find exactly what you need and get instant install configs.

## Features

- **Search** — Find MCP servers by keyword, capability or category
- **Browse** — Explore 50+ servers across 15+ categories
- **Install** — Get copy-paste configs for any MCP client
- **Submit** — Add your own servers to the catalog (community-driven)
- **Persistent** — Catalog grows with community submissions

## Installation

```bash
pip install mcp-hub-server
```

## Usage with Claude Code

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "hub": {
      "command": "uvx",
      "args": ["mcp-hub-server"]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `search_servers` | Search for servers by keyword |
| `get_server_details` | Full details + install config |
| `list_categories` | Browse all categories |
| `list_servers` | List servers (optionally by category) |
| `submit_server` | Add a new server to the catalog |
| `get_install_config` | Get copy-paste JSON config |

## Examples

```
"Find me an MCP server for weather data"
"What database servers are available?"
"How do I install the GitHub MCP server?"
"Show me all crypto and DeFi servers"
"List all categories"
```

## Pre-loaded Catalog

Ships with 50+ servers including:
- **Official Anthropic servers** (GitHub, Filesystem, PostgreSQL, etc.)
- **Company servers** (Stripe, Notion, Linear, Docker, Sentry)
- **Community servers** across Crypto, Weather, Space, Agriculture and more

## Contributing

Submit new servers directly through the `submit_server` tool, or open a PR to add servers to the built-in catalog.


---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| 🔗 Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| 🌍 Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| 🔒 Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| 🤖 Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) |
| 🔬 Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) |

[→ Full catalog (40+ servers)](https://github.com/AiAgentKarl)

## License

MIT
