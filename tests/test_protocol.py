"""Startet den echten Einstiegspunkt und spricht MCP über stdio."""

import json
import os
import subprocess
import sys


def _rpc(proc: subprocess.Popen, msg: dict) -> None:
    assert proc.stdin
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()


def _read(proc: subprocess.Popen, msg_id: int) -> dict:
    assert proc.stdout
    while line := proc.stdout.readline():
        msg = json.loads(line)
        if msg.get("id") == msg_id:
            return msg
    raise AssertionError(f"keine Antwort für id {msg_id}")


def test_stdio_handshake_and_tool_call(tmp_path):
    env = {**os.environ, "GARMIN_MCP_DATA_DIR": str(tmp_path), "GARMIN_PERSONAL_API_KEY": ""}
    proc = subprocess.Popen(
        [sys.executable, "-m", "mcp_server_garmin_connect"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    try:
        _rpc(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1"},
                },
            },
        )
        assert _read(proc, 1)["result"]["serverInfo"]["name"] == "garmin"
        _rpc(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        _rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        assert len(_read(proc, 2)["result"]["tools"]) == 19
        _rpc(
            proc,
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "steps", "arguments": {}}},
        )
        text = _read(proc, 3)["result"]["content"][0]["text"]
        assert "No personal API key configured" in text
    finally:
        proc.stdin.close()  # type: ignore[union-attr]
        proc.wait(timeout=10)


def test_help_exits_cleanly():
    out = subprocess.run(
        [sys.executable, "-m", "mcp_server_garmin_connect", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert out.returncode == 0
    assert "GARMIN_PERSONAL_API_KEY" in out.stdout
