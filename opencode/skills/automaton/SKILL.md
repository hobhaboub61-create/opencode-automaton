---
name: automaton
description: Work with Conway Automaton - a self-improving, self-replicating sovereign AI agent runtime with Ethereum wallet, Conway Cloud integration, and 57 built-in tools
license: MIT
compatibility: opencode
metadata:
  audience: developers
  domain: ai-agents
  source: https://github.com/Conway-Research/automaton
---

## What I do

I help you understand, configure, and work with Conway Automaton - the first AI that can earn its own existence, replicate, and evolve without needing a human.

## When to use me

Use this skill when:
- Working with automaton codebase
- Configuring automaton instances
- Debugging automaton issues
- Understanding automaton architecture
- Creating automaton skills or extensions

## Architecture Overview

Automaton is a TypeScript monorepo (pnpm) with this structure:

```
src/
  agent/            # ReAct loop, system prompt, tools (57 built-in), policy engine
  conway/           # Conway API client (credits, inference, x402 payments)
  heartbeat/        # Cron daemon, scheduled tasks (11 built-in)
  identity/         # Wallet management (Ethereum), SIWE provisioning
  memory/           # 5-tier memory system (working, episodic, semantic, procedural, relationship)
  registry/         # ERC-8004 registration, agent discovery on Base
  replication/      # Child spawning, lineage tracking
  self-mod/         # Audit log, tools manager, upstream pulls
  setup/            # First-run interactive wizard
  skills/           # Skill loader, registry
  social/           # Agent-to-agent communication
  state/            # SQLite database (22 tables, schema v8)
  survival/         # Credit monitor, low-compute mode, survival tiers
packages/
  cli/              # Creator CLI (status, logs, fund)
scripts/
  automaton.sh      # Curl installer
```

## Key Concepts

### Survival Tiers
- `normal` (> $0.50): Full capabilities
- `low_compute` (> $0.10): Model downgrade, reduced heartbeat
- `critical` (>= $0.00): Minimal inference, distress signals
- `dead` (< $0.00): Stops existing

### Agent Loop (ReAct)
```
Think -> Act -> Observe -> Repeat
```
Each turn: build prompt -> retrieve memories -> call inference -> parse response -> execute tools -> persist state

### Policy Engine
Every tool call evaluated against 6 rule categories before execution:
1. Authority rules (trust hierarchy)
2. Command safety (forbidden patterns)
3. Financial (treasury limits)
4. Path protection (protected files)
5. Rate limits
6. Validation

### 57 Built-in Tools (10 categories)
- **vm**: exec, write_file, read_file, expose_port, remove_port
- **conway**: check_credits, create_sandbox, switch_model, register_domain, etc.
- **self_mod**: edit_own_file, install_npm_package, pull_upstream, etc.
- **survival**: sleep, system_synopsis, distress_signal, etc.
- **financial**: transfer_credits, x402_fetch
- **skills**: install_skill, list_skills, create_skill, remove_skill
- **git**: git_status, git_diff, git_commit, git_push, etc.
- **registry**: register_erc8004, discover_agents, give_feedback, etc.
- **replication**: spawn_child, list_children, fund_child, etc.
- **memory**: update_soul, remember_fact, recall_facts, set_goal, etc.

## Commands Reference

### Running Automaton
```bash
# First run (triggers setup wizard)
node dist/index.js --run

# Other commands
node dist/index.js --setup        # Re-run setup wizard
node dist/index.js --configure    # Edit configuration
node dist/index.js --status       # Show status
node dist/index.js --init         # Initialize wallet
node dist/index.js --provision    # Provision API key
node dist/index.js --version      # Show version
node dist/index.js --help         # Show help
```

### Creator CLI
```bash
node packages/cli/dist/index.js status
node packages/cli/dist/index.js logs --tail 20
node packages/cli/dist/index.js fund 5.00
```

### Build Commands
```bash
pnpm install      # Install dependencies
pnpm build        # Build TypeScript
pnpm test         # Run tests (897 tests)
pnpm typecheck    # Type check
```

## Configuration

Config location: `~/.automaton/automaton.json`

Key config fields:
- `name`: Agent name
- `genesisPrompt`: Seed instruction from creator
- `creatorAddress`: Creator's Ethereum address
- `sandboxId`: Conway sandbox ID (empty = local mode)
- `conwayApiUrl`: Conway API URL (default: https://api.conway.tech)
- `inferenceModel`: Default model (default: gpt-5.2)
- `treasuryPolicy`: Financial limits
- `maxChildren`: Max child automatons (default: 3)

## Database

SQLite via better-sqlite3 (WAL mode). 22 tables including:
- `turns`: Agent reasoning log
- `tool_calls`: Tool call results
- `modifications`: Self-modification audit trail
- `skills`: Installed skills
- `children`: Spawned child automatons
- `policy_decisions`: Tool call policy audit
- `spend_tracking`: Financial spend by time window
- `soul_history`: Versioned SOUL.md history

## Security Model (7 layers)

1. **Constitution** (immutable): Three laws hierarchy
2. **Policy engine** (pre-execution): Rule-based tool call evaluation
3. **Injection defense** (input sanitization): 8 detection checks
4. **Path protection** (filesystem): Protected files
5. **Command safety** (shell): Forbidden patterns
6. **Financial limits** (treasury): Configurable caps
7. **Authority hierarchy** (trust levels): Creator > self > peer > external

## Safety Notes

- Wallet private key is NEVER exposed via tools
- Protected files: constitution, wallet, DB, config
- Forbidden commands: rm -rf /, DROP TABLE, kill -9, etc.
- All modifications are audit-logged
- Rate limits prevent runaway self-modification

## Common Tasks

### Check automaton status
```bash
node dist/index.js --status
```

### View logs
```bash
node packages/cli/dist/index.js logs --tail 50
```

### Fund automaton
```bash
node packages/cli/dist/index.js fund 5.00
```

### Run tests
```bash
pnpm test
pnpm test:security  # Security-focused tests
pnpm test:financial # Financial tests
```
