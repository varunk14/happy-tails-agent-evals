"""Minimal client for a published Agentplace agent's MCP endpoint (<agent-url>/mcp).

Streamable HTTP, JSON-RPC 2.0. Uses only the standard library. Tools exposed by Agentplace
(verified 11 Nov 2026): askAgent(message, sessionId), createSession(), getConversationHistory(
sessionId, limit), getAgentInfo().
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

PROTOCOL = "2025-06-18"


class MCPError(RuntimeError):
    pass


class AgentMCP:
    def __init__(self, agent_url: str, timeout: float = 240.0):
        self.url = agent_url.rstrip("/") + "/mcp"
        self.timeout = timeout
        self.session_id: str | None = None
        self._next_id = 0

    def _post(self, payload: dict) -> list[dict]:
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                sid = resp.headers.get("mcp-session-id")
                if sid:
                    self.session_id = sid
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise MCPError(f"HTTP {e.code}: {e.read()[:300]!r}") from e
        if not body.strip():
            return []  # e.g. 202 Accepted for notifications
        msgs = [json.loads(line[5:].strip()) for line in body.splitlines() if line.startswith("data:")]
        return msgs or [json.loads(body)]

    def _rpc(self, method: str, params: dict | None = None) -> dict:
        self._next_id += 1
        rid = self._next_id
        for msg in self._post({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}}):
            if msg.get("id") == rid:
                if "error" in msg:
                    raise MCPError(f"{method}: {msg['error']}")
                return msg["result"]
        raise MCPError(f"{method}: no matching response")

    def connect(self) -> dict:
        info = self._rpc("initialize", {"protocolVersion": PROTOCOL, "capabilities": {},
                                        "clientInfo": {"name": "happytails-eval-harness", "version": "1.0"}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return info

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self._rpc("tools/call", {"name": name, "arguments": arguments})

    def agent_info(self) -> dict:
        r = self.call_tool("getAgentInfo", {})
        return {"text": [c.get("text", "") for c in r.get("content", []) if c.get("type") == "text"], "raw": r}

    def ask(self, message: str, conversation_id: str) -> dict:
        """Send one customer turn. Returns the agent's text blocks (reply text + card text) and latency."""
        t0 = time.monotonic()
        r = self.call_tool("askAgent", {"message": message, "sessionId": conversation_id})
        return {
            "blocks": [c.get("text", "") for c in r.get("content", []) if c.get("type") == "text"],
            "is_error": bool(r.get("isError")),
            "latency_s": round(time.monotonic() - t0, 2),
        }

    def history(self, conversation_id: str, limit: int = 100) -> dict:
        return self.call_tool("getConversationHistory", {"sessionId": conversation_id, "limit": limit})
