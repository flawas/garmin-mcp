#!/bin/sh
# Startet den MCP-Server des Plugins garmin-connect.
#  1. Mit uv (bevorzugt): Abhängigkeiten und bei Bedarf Python 3.12+ werden automatisch geladen.
#  2. Ohne uv: venv mit vorhandenem Python >= 3.12 im Plugin-Datenordner (einmalig).
# stdout gehört dem MCP-Protokoll – alle Ausgaben dieses Scripts gehen nach stderr.
set -eu

ROOT="$CLAUDE_PLUGIN_ROOT"
DATA="$CLAUDE_PLUGIN_DATA"
mkdir -p "$DATA"
export GARMIN_MCP_DATA_DIR="$DATA"

# Von GUI-Apps gestartete Prozesse haben auf macOS nur einen minimalen PATH
PATH="$HOME/.local/bin:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
export PATH

log() { echo "[garmin-mcp] $*" >&2; }

if command -v uv >/dev/null 2>&1; then
  exec uv run --quiet --script "$ROOT/garmin_mcp.py"
fi

PY=""
for candidate in python3.14 python3.13 python3.12 python3; do
  if command -v "$candidate" >/dev/null 2>&1 &&
    "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then
    PY="$(command -v "$candidate")"
    break
  fi
done

if [ -z "$PY" ]; then
  log "Weder uv noch Python >= 3.12 gefunden."
  log "Installiere uv (empfohlen): brew install uv   oder   curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

VENV="$DATA/venv"
STAMP="$VENV/.requirements.txt"
if [ ! -x "$VENV/bin/python" ] || ! cmp -s "$ROOT/requirements.txt" "$STAMP"; then
  log "Richte Python-Umgebung ein (einmalig, mit $PY) ..."
  "$PY" -m venv "$VENV" >&2
  "$VENV/bin/python" -m pip install --quiet --disable-pip-version-check -r "$ROOT/requirements.txt" >&2
  cp "$ROOT/requirements.txt" "$STAMP"
fi

exec "$VENV/bin/python" "$ROOT/garmin_mcp.py"
