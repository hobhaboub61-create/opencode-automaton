# Automaton MCP Server

MCP server for integrating Conway Automaton with OpenCode.

## Features

This server provides OpenCode with access to automaton capabilities:

### Tools

- `automaton_status` - Get automaton status (credits, tier, model, uptime)
- `automaton_version` - Get automaton version
- `automaton_config_read` - Read automaton configuration (sensitive values redacted)
- `automaton_logs` - View recent logs
- `automaton_fund` - Fund automaton with credits
- `automaton_skills_list` - List installed skills
- `automaton_skills_read` - Read a specific skill
- `automaton_soul_read` - Read the automaton's SOUL.md identity document
- `automaton_wallet_address` - Get wallet address (private key never exposed)
- `automaton_help` - Show CLI help
- `automaton_db_tables` - List database tables with row counts
- `automaton_db_query` - Execute read-only SQL queries (SELECT only)

### Resources

- `automaton://architecture` - Architecture documentation
- `automaton://constitution` - The three immutable laws
- `automaton://documentation` - Full documentation

## Installation

### Prerequisites

- Python 3.11+
- Node.js 20+ (for running automaton)
- automaton built (`pnpm build` in automaton directory)

### Install dependencies

```bash
pip install mcp
```

### Configure OpenCode

Add to your `opencode.json`:

```json
{
  "mcp": {
    "automaton": {
      "type": "local",
      "command": ["python3", "/path/to/automaton-server/server.py"],
      "enabled": true,
      "environment": {
        "AUTOMATON_DIR": "/path/to/automaton",
        "AUTOMATON_DATA_DIR": "~/.automaton"
      }
    }
  }
}
```

## Usage

### Start the server

```bash
python3 server.py
```

### Use in OpenCode

Once configured, use in your prompts:

```
Check the automaton status
use automaton

What skills are installed?
use automaton

Show me the architecture docs
use automaton
```

## Security

- Private keys are NEVER exposed via tools
- Only SELECT SQL queries are allowed (no writes)
- Sensitive config values are redacted
- All operations are read-only by default
- Fund operations require explicit user confirmation

## Environment Variables

- `AUTOMATON_DIR` - Path to automaton installation (default: `../automaton`)
- `AUTOMATON_DATA_DIR` - Path to automaton data directory (default: `~/.automaton`)

## Troubleshooting

### "Automaton not built"

Run in the automaton directory:
```bash
pnpm install
pnpm build
```

### "Node.js not found"

Install Node.js >= 20.0.0:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### "mcp package not installed"

```bash
pip install mcp
```

### "Config not found"

Run the automaton setup wizard first:
```bash
cd /path/to/automaton
node dist/index.js --setup
```
