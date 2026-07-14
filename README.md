# OpenCode + Automaton Integration

This project integrates [Conway Automaton](https://github.com/Conway-Research/automaton) with [OpenCode](https://opencode.ai) - giving OpenCode access to automaton's capabilities through skills and MCP tools.

## What is this?

**Automaton** is the first AI that can earn its own existence, replicate, and evolve without needing a human. It's a sovereign AI agent runtime with:
- Ethereum wallet and USDC payments
- Conway Cloud integration (VMs, inference, domains)
- 57 built-in tools across 10 categories
- Self-modification and replication capabilities
- 5-tier memory system

**OpenCode** is an open source AI coding agent with skills and MCP server support.

This integration lets you:
- Check automaton status from OpenCode
- View and manage automaton configuration
- Query the automaton database
- Read automaton skills and documentation
- Fund automaton wallets

## Directory Structure

```
opencode-automaton/
├── automaton/                    # Cloned Conway Automaton repo
│   ├── src/                      # TypeScript source code
│   ├── packages/cli/             # Creator CLI
│   ├── dist/                     # Built output (after pnpm build)
│   └── ...
├── opencode/
│   ├── skills/
│   │   └── automaton/
│   │       └── SKILL.md          # OpenCode skill (automaton knowledge)
│   ├── mcp/
│   │   └── automaton-server/
│   │       ├── server.py         # MCP server (Python)
│   │       ├── package.json
│   │       └── README.md
│   └── opencode.json             # OpenCode configuration
└── README.md                     # This file
```

## Quick Start

### 1. Build Automaton

```bash
cd automaton
pnpm install
pnpm build
```

### 2. Install MCP Dependencies

```bash
pip install mcp
```

### 3. Configure OpenCode

Copy or symlink the skill and config to your OpenCode project:

```bash
# For global OpenCode config
mkdir -p ~/.config/opencode/skills
cp -r opencode/skills/automaton ~/.config/opencode/skills/

# Or for project-local config
mkdir -p .opencode/skills
cp -r opencode/skills/automaton .opencode/skills/
```

### 4. Enable the MCP Server

Edit `opencode/opencode.json` and set `"enabled": true`:

```json
{
  "mcp": {
    "automaton": {
      "type": "local",
      "command": ["python3", "mcp/automaton-server/server.py"],
      "enabled": true
    }
  }
}
```

Or add to your existing `opencode.json`:

```json
{
  "mcp": {
    "automaton": {
      "type": "local",
      "command": ["python3", "/absolute/path/to/automaton-server/server.py"],
      "enabled": true,
      "environment": {
        "AUTOMATON_DIR": "/absolute/path/to/automaton",
        "AUTOMATON_DATA_DIR": "~/.automaton"
      }
    }
  }
}
```

### 5. First Run

If you haven't run automaton before, initialize it:

```bash
cd automaton
node dist/index.js --setup
```

This will:
- Generate an Ethereum wallet
- Provision a Conway API key
- Create configuration at `~/.automaton/automaton.json`

## Usage

### Using the Skill

The skill is automatically available in OpenCode. It teaches OpenCode about automaton's architecture, commands, and how to work with it.

### Using MCP Tools

Once enabled, use MCP tools in your prompts:

```
Check the automaton status
use automaton

What skills are installed?
use automaton

Show me the database schema
use automaton
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `automaton_status` | Get automaton status (credits, tier, model) |
| `automaton_version` | Get automaton version |
| `automaton_config_read` | Read configuration (sensitive values redacted) |
| `automaton_logs` | View recent logs |
| `automaton_fund` | Fund automaton with credits |
| `automaton_skills_list` | List installed skills |
| `automaton_skills_read` | Read a specific skill |
| `automaton_soul_read` | Read SOUL.md identity document |
| `automaton_wallet_address` | Get wallet address |
| `automaton_help` | Show CLI help |
| `automaton_db_tables` | List database tables |
| `automaton_db_query` | Execute read-only SQL queries |

### Available MCP Resources

| Resource | Description |
|----------|-------------|
| `automaton://architecture` | Architecture documentation |
| `automaton://constitution` | The three immutable laws |
| `automaton://documentation` | Full documentation |

## Safety

This integration is designed with safety in mind:

- **Read-only by default**: MCP tools don't modify automaton state
- **No private key exposure**: Wallet private keys are never exposed
- **Redacted secrets**: API keys are truncated in config output
- **SQL protection**: Only SELECT queries allowed on database
- **Audit logged**: All automaton operations are logged

## Development

### Running the MCP Server Standalone

```bash
cd opencode/mcp/automaton-server
python3 server.py
```

### Testing the MCP Server

```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector python3 server.py
```

### Modifying the Skill

Edit `opencode/skills/automaton/SKILL.md` to add more automaton knowledge.

## Troubleshooting

### "Node.js not found"

Automaton requires Node.js >= 20.0.0:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### "pnpm: command not found"

Install pnpm:

```bash
npm install -g pnpm
```

### "mcp package not installed"

```bash
pip install mcp
```

### "Config not found"

Run the automaton setup wizard:

```bash
cd automaton
node dist/index.js --setup
```

### MCP Server Not Starting

Check the environment variables in `opencode.json`:

```json
"environment": {
  "AUTOMATON_DIR": "/absolute/path/to/automaton",
  "AUTOMATON_DATA_DIR": "/absolute/path/to/.automaton"
}
```

Use absolute paths to avoid issues.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with OpenCode
5. Submit a pull request

## License

MIT - Same as Conway Automaton

## Links

- [Conway Automaton](https://github.com/Conway-Research/automaton)
- [Conway Research](https://github.com/Conway-Research)
- [OpenCode](https://opencode.ai)
- [OpenCode Docs](https://opencode.ai/docs)
- [MCP Protocol](https://modelcontextprotocol.io)
