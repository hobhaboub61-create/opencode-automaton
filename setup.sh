#!/bin/bash
# OpenCode + Automaton Setup Script
# This script helps set up the integration

set -e

echo "=== OpenCode + Automaton Setup ==="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js >= 20.0.0"
    echo "   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -"
    echo "   sudo apt-get install -y nodejs"
    exit 1
fi
echo "✓ Node.js $(node --version)"

# Check pnpm
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm not found. Installing..."
    npm install -g pnpm
fi
echo "✓ pnpm $(pnpm --version)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi
echo "✓ Python $(python3 --version 2>&1 | cut -d' ' -f2)"

# Check mcp package
if ! python3 -c "import mcp" 2>/dev/null; then
    echo "⚠️  mcp package not found. Installing..."
    pip install mcp
fi
echo "✓ mcp package"

echo ""
echo "=== Building Automaton ==="
cd automaton
pnpm install
pnpm build
cd ..

echo ""
echo "=== Setting up OpenCode Skill ==="
# Create global skills directory
mkdir -p ~/.config/opencode/skills
cp -r opencode/skills/automaton ~/.config/opencode/skills/
echo "✓ Skill installed to ~/.config/opencode/skills/automaton"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Initialize automaton (first run):"
echo "   cd automaton && node dist/index.js --setup"
echo ""
echo "2. Enable MCP server in opencode.json:"
echo "   Set 'enabled': true for the automaton MCP server"
echo ""
echo "3. Use in OpenCode:"
echo "   'Check automaton status' + use automaton"
echo ""
echo "For more info, see README.md"
