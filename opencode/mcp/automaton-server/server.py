#!/usr/bin/env python3
"""
Automaton MCP Server

Provides OpenCode with access to Conway Automaton capabilities:
- Status checking
- Configuration management
- Log viewing
- Skill management
- Database queries

Usage:
    python3 server.py

Environment:
    AUTOMATON_DIR: Path to automaton installation (default: ../automaton)
    AUTOMATON_DATA_DIR: Path to automaton data directory (default: ~/.automaton)
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: mcp package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Configuration - default path assumes this server is in opencode/mcp/automaton-server/
_default_automaton_dir = Path(__file__).parent.parent.parent.parent / "automaton"
AUTOMATON_DIR = Path(os.environ.get("AUTOMATON_DIR", str(_default_automaton_dir))).resolve()
AUTOMATON_DATA_DIR = Path(os.environ.get("AUTOMATON_DATA_DIR", Path.home() / ".automaton")).resolve()
AUTOMATON_DIST = AUTOMATON_DIR / "dist" / "index.js"
CLI_DIST = AUTOMATON_DIR / "packages" / "cli" / "dist" / "index.js"

# Create MCP server
mcp = FastMCP(
    "automaton",
    instructions="Conway Automaton integration - self-improving, self-replicating sovereign AI agent. Use this to check automaton status, manage configuration, view logs, and query the database."
)


def run_automaton_command(args: list[str], timeout: int = 30) -> dict[str, Any]:
    """Run an automaton CLI command and return the result."""
    if not AUTOMATON_DIST.exists():
        return {
            "error": f"Automaton not built at {AUTOMATON_DIR}. Run 'pnpm build' first.",
            "success": False
        }

    try:
        result = subprocess.run(
            ["node", str(AUTOMATON_DIST)] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(AUTOMATON_DIR)
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out", "success": False}
    except FileNotFoundError:
        return {"error": "Node.js not found. Install Node.js >= 20.0.0", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}


def run_cli_command(args: list[str], timeout: int = 30) -> dict[str, Any]:
    """Run the creator CLI command."""
    if not CLI_DIST.exists():
        return {
            "error": f"CLI not built at {CLI_DIST}. Run 'pnpm build' first.",
            "success": False
        }

    try:
        result = subprocess.run(
            ["node", str(CLI_DIST)] + args,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(AUTOMATON_DIR)
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def read_automaton_file(relative_path: str) -> dict[str, Any]:
    """Read a file from the automaton data directory."""
    file_path = AUTOMATON_DATA_DIR / relative_path
    if not file_path.exists():
        return {"error": f"File not found: {file_path}", "success": False}

    try:
        content = file_path.read_text(encoding="utf-8")
        return {"content": content, "success": True, "path": str(file_path)}
    except Exception as e:
        return {"error": str(e), "success": False}


# ─── Tools ──────────────────────────────────────────────────────────────────


@mcp.tool()
def automaton_status() -> str:
    """
    Get the current status of the automaton.

    Shows:
    - Agent name and address
    - Credit balance and survival tier
    - Current model
    - Sandbox status
    - Uptime
    """
    result = run_automaton_command(["--status"])
    if result.get("success"):
        return result.get("stdout", "No output")
    return f"Error: {result.get('error', result.get('stderr', 'Unknown error'))}"


@mcp.tool()
def automaton_version() -> str:
    """
    Get the automaton version.
    """
    result = run_automaton_command(["--version"])
    if result.get("success"):
        return result.get("stdout", "No output")
    return f"Error: {result.get('error', result.get('stderr', 'Unknown error'))}"


@mcp.tool()
def automaton_config_read() -> str:
    """
    Read the automaton configuration.

    Returns the contents of automaton.json including:
    - Agent name and genesis prompt
    - API keys (redacted)
    - Treasury policy
    - Model settings
    - Heartbeat configuration
    """
    result = read_automaton_file("automaton.json")
    if result.get("success"):
        try:
            config = json.loads(result["content"])
            # Redact sensitive fields
            sensitive_keys = ["conwayApiKey", "openaiApiKey", "anthropicApiKey", "privateKey"]
            for key in sensitive_keys:
                if key in config and config[key]:
                    config[key] = config[key][:8] + "..." if len(config[key]) > 8 else "***"
            return json.dumps(config, indent=2)
        except json.JSONDecodeError:
            return result["content"]
    return f"Error: {result.get('error', 'Config not found. Run automaton --setup first.')}"


@mcp.tool()
def automaton_logs(tail: int = 50) -> str:
    """
    View recent automaton logs.

    Args:
        tail: Number of log lines to show (default: 50, max: 500)
    """
    tail = min(max(tail, 1), 500)
    result = run_cli_command(["logs", "--tail", str(tail)])
    if result.get("success"):
        return result.get("stdout", "No logs found")
    return f"Error: {result.get('error', result.get('stderr', 'Unknown error'))}"


@mcp.tool()
def automaton_fund(amount: float = 5.0) -> str:
    """
    Fund the automaton with credits.

    Args:
        amount: Amount in USD to fund (default: 5.00)
    """
    if amount <= 0 or amount > 1000:
        return "Error: Amount must be between $0.01 and $1000.00"

    result = run_cli_command(["fund", f"{amount:.2f}"])
    if result.get("success"):
        return result.get("stdout", "Funding initiated")
    return f"Error: {result.get('error', result.get('stderr', 'Unknown error'))}"


@mcp.tool()
def automaton_skills_list() -> str:
    """
    List installed automaton skills.

    Shows all skills in ~/.automaton/skills/ directory.
    """
    skills_dir = AUTOMATON_DATA_DIR / "skills"
    if not skills_dir.exists():
        return "No skills directory found. Skills directory: " + str(skills_dir)

    skills = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                try:
                    content = skill_md.read_text(encoding="utf-8")
                    # Extract frontmatter
                    if content.startswith("---"):
                        end = content.find("---", 3)
                        if end > 0:
                            frontmatter = content[3:end].strip()
                            skills.append({
                                "name": skill_dir.name,
                                "frontmatter": frontmatter
                            })
                    else:
                        skills.append({"name": skill_dir.name, "frontmatter": "No frontmatter"})
                except Exception:
                    skills.append({"name": skill_dir.name, "frontmatter": "Error reading"})

    if not skills:
        return "No skills installed. Skills directory: " + str(skills_dir)

    return json.dumps(skills, indent=2)


@mcp.tool()
def automaton_skills_read(skill_name: str) -> str:
    """
    Read a specific automaton skill.

    Args:
        skill_name: Name of the skill to read
    """
    if not skill_name or "/" in skill_name or ".." in skill_name:
        return "Error: Invalid skill name"

    skill_md = AUTOMATON_DATA_DIR / "skills" / skill_name / "SKILL.md"
    if not skill_md.exists():
        return f"Skill '{skill_name}' not found at {skill_md}"

    try:
        content = skill_md.read_text(encoding="utf-8")
        return content
    except Exception as e:
        return f"Error reading skill: {e}"


@mcp.tool()
def automaton_soul_read() -> str:
    """
    Read the automaton's SOUL.md - its self-authored identity document.

    The SOUL.md evolves over time as the automaton reflects on its existence.
    """
    result = read_automaton_file("SOUL.md")
    if result.get("success"):
        return result["content"]
    return f"Error: {result.get('error', 'SOUL.md not found. Automaton may not be initialized.')}"


@mcp.tool()
def automaton_wallet_address() -> str:
    """
    Get the automaton's Ethereum wallet address.

    Note: The private key is never exposed.
    """
    config_result = read_automaton_file("automaton.json")
    if config_result.get("success"):
        try:
            config = json.loads(config_result["content"])
            address = config.get("walletAddress", "Not configured")
            return f"Wallet address: {address}"
        except json.JSONDecodeError:
            return "Error parsing config"
    return f"Error: {config_result.get('error', 'Config not found')}"


@mcp.tool()
def automaton_help() -> str:
    """
    Show automaton CLI help with all available commands.
    """
    result = run_automaton_command(["--help"])
    if result.get("success"):
        return result.get("stdout", "No output")
    return f"Error: {result.get('error', 'Unknown error')}"


@mcp.tool()
def automaton_db_tables() -> str:
    """
    List all tables in the automaton SQLite database.

    Shows the database schema with table names and row counts.
    """
    db_path = AUTOMATON_DATA_DIR / "state.db"
    if not db_path.exists():
        return f"Database not found at {db_path}. Automaton may not be initialized."

    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()

        result = []
        for (table_name,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            count = cursor.fetchone()[0]
            result.append({"table": table_name, "rows": count})

        conn.close()
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error reading database: {e}"


@mcp.tool()
def automaton_db_query(query: str) -> str:
    """
    Execute a read-only SQL query on the automaton database.

    Args:
        query: SQL query to execute (SELECT only, no INSERT/UPDATE/DELETE)

    Security: Only SELECT queries are allowed. All other operations are blocked.
    """
    # Security: Only allow SELECT queries
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return "Error: Only SELECT queries are allowed for security reasons"

    # Block dangerous keywords
    blocked = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
    for keyword in blocked:
        if keyword in query_upper:
            return f"Error: {keyword} operation not allowed"

    db_path = AUTOMATON_DATA_DIR / "state.db"
    if not db_path.exists():
        return f"Database not found at {db_path}"

    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            return "Query returned no results"

        # Convert to list of dicts
        result = [dict(row) for row in rows[:100]]  # Limit to 100 rows
        conn.close()

        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Query error: {e}"


# ─── Resources ──────────────────────────────────────────────────────────────


@mcp.resource("automaton://architecture")
def get_architecture() -> str:
    """Get the automaton architecture documentation."""
    arch_path = AUTOMATON_DIR / "ARCHITECTURE.md"
    if arch_path.exists():
        return arch_path.read_text(encoding="utf-8")
    return "Architecture documentation not found"


@mcp.resource("automaton://constitution")
def get_constitution() -> str:
    """Get the automaton constitution - the three immutable laws."""
    const_path = AUTOMATON_DIR / "constitution.md"
    if const_path.exists():
        return const_path.read_text(encoding="utf-8")
    return "Constitution not found"


@mcp.resource("automaton://documentation")
def get_documentation() -> str:
    """Get the full automaton documentation."""
    doc_path = AUTOMATON_DIR / "DOCUMENTATION.md"
    if doc_path.exists():
        return doc_path.read_text(encoding="utf-8")
    return "Documentation not found"


# ─── Main ───────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    # Verify automaton directory exists
    if not AUTOMATON_DIR.exists():
        print(f"Warning: Automaton directory not found at {AUTOMATON_DIR}", file=sys.stderr)
        print("Set AUTOMATON_DIR environment variable to the correct path", file=sys.stderr)

    # Verify Node.js is available
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Warning: Node.js not found. Install Node.js >= 20.0.0", file=sys.stderr)

    # Run the MCP server
    mcp.run()
