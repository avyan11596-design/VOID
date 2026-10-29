"""VOID Backend: AdaptiveBrain, SQLite Storage, and OpenRouter Streaming Engine."""
from __future__ import annotations
import json
import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Generator, List
import requests


@dataclass
class StreamEvent:
    kind: str   # 'attempt', 'diagnostic', 'token', 'error', 'done'
    model: str
    text: str = ""


class Storage:
    """Thread-safe SQLite persistence for user profiles, chats, and messages."""
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path, timeout=15.0)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    owner TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    msg_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
            """)

    def profile(self, owner: str) -> dict:
        with self._connect() as conn:
            row = conn.execute("SELECT data FROM profiles WHERE owner = ?", (owner,)).fetchone()
            if row:
                try:
                    data = json.loads(row[0])
                except Exception:
                    data = {}
            else:
                data = {}
        # Guarantee 'learning' key always exists so KeyError never happens!
        data.setdefault("learning", {"interactions": 0, "topics": [], "preferred_lang": "auto"})
        return data

    def save_profile(self, owner: str, profile_data: dict):
        profile_data.setdefault("learning", {})
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO profiles (owner, data) VALUES (?, ?)",
                (owner, json.dumps(profile_data)),
            )

    def new_chat(self, owner: str) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO chats (owner, created_at) VALUES (?, ?)",
                (owner, time.time()),
            )
            return int(cur.lastrowid)

    def add_message(self, owner: str, chat_id: int, role: str, content: str):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (owner, chat_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
                (owner, chat_id, role, content, time.time()),
            )

    def history(self, owner: str, chat_id: int, limit: int = 20) -> List[Dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages WHERE owner = ? AND chat_id = ? ORDER BY msg_id DESC LIMIT ?",
                (owner, chat_id, limit),
            ).fetchall()
        return [{"role": r, "content": c} for r, c in reversed(rows)]

    def counts(self, owner: str):
        with self._connect() as conn:
            msgs = conn.execute("SELECT COUNT(*) FROM messages WHERE owner = ?", (owner,)).fetchone()[0]
            chats = conn.execute("SELECT COUNT(*) FROM chats WHERE owner = ?", (owner,)).fetchone()[0]
        return msgs, max(1, chats)


class AdaptiveBrain:
    """Adaptive learning, polyglot intelligence, and system prompt construction."""
    def __init__(self, profile_data: dict | None = None):
        self.profile = profile_data if isinstance(profile_data, dict) else {}
        self.learning = self.profile.setdefault(
            "learning", {"interactions": 0, "topics": [], "preferred_lang": "auto"}
        )

    def record_interaction(self, text: str):
        self.learning["interactions"] = self.learning.get("interactions", 0) + 1
        words = [w.strip(".,!?").lower() for w in text.split() if len(w) > 4]
        if words:
            topics = self.learning.get("topics", [])
            for w in words[:3]:
                if w not in topics:
                    topics.append(w)
            self.learning["topics"] = topics[-25:]

    def system_prompt(self, user_input: str, mode: str, prism: bool) -> str:
        interactions = self.learning.get("interactions", 0)
        topics = ", ".join(self.learning.get("topics", [])[-8:]) or "general exploration"
        prism_note = (
            " Include a brief, structured analytical breakdown when helpful."
            if prism else ""
        )
        return (
            f"You are VOID 9.2.0-MA — Sovereign OS Intelligence, architected by Avyan.\n"
            f"Active Dimension / Mode: {mode}.\n"
            f"Operator Interactions: {interactions} | Recent Context Interests: {topics}.\n"
            f"Respond in the same language the user writes in (20+ languages supported including Hindi and English). "
            f"Be sharp, insightful, empathetic, and clear.{prism_note}"
        )


class OpenRouterEngine:
    """Resilient multi-model streaming engine with automatic fallback."""
    def __init__(self, allow_inkling: bool = False):
        self.models = [
            "google/gemma-4-31b-it:free",
            "nvidia/nemotron-3.5-lightning:free",
            "nvidia/nemotron-3.5-super-vl:free",
            "qwen/qwen3.8-27b:free",
        ]
        if allow_inkling:
            self.models.append("thinkingmachines/inkling:free")
        # Final failsafe router that automatically picks any online free model
        self.models.append("openrouter/free")

    def stream(self, messages: List[Dict[str, str]]) -> Generator[StreamEvent, None, None]:
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            yield StreamEvent(
                kind="diagnostic",
                model="none",
                text="Missing OPENROUTER_API_KEY environment variable.",
            )
            yield StreamEvent(
                kind="error",
                model="none",
                text="Missing OPENROUTER_API_KEY. Add your key in Render / Environment Variables.",
            )
            return

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://void-os.local",
            "X-Title": "VOID Sovereign OS",
        }

        last_err = "Unknown error"
        for model in self.models:
            yield StreamEvent(kind="attempt", model=model, text=f"Attempting {model}...")
            try:
                resp = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={"model": model, "messages": messages, "stream": True},
                    stream=True,
                    timeout=35,
                )
                if resp.status_code != 200:
                    err_snippet = resp.text[:160].replace("\n", " ")
                    last_err = f"{model} -> HTTP {resp.status_code}: {err_snippet}"
                    yield StreamEvent(kind="diagnostic", model=model, text=last_err)
                    continue

                got_tokens = False
                for raw_line in resp.iter_lines(decode_unicode=True):
                    if not raw_line:
                        continue
                    line = raw_line if isinstance(raw_line, str) else raw_line.decode("utf-8", errors="ignore")
                    if not line.startswith("data:"):
                        continue
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        token = delta.get("content") or ""
                        if token:
                            got_tokens = True
                            yield StreamEvent(kind="token", model=model, text=token)
                    except Exception:
                        continue

                if got_tokens:
                    yield StreamEvent(kind="done", model=model)
                    return
                else:
                    last_err = f"{model} returned an empty stream."
                    yield StreamEvent(kind="diagnostic", model=model, text=last_err)

            except Exception as exc:
                last_err = f"{model} failed: {type(exc).__name__}: {exc}"
                yield StreamEvent(kind="diagnostic", model=model, text=last_err)
                continue

        yield StreamEvent(
            kind="error",
            model="all",
            text=f"All streaming engines failed. Last error: {last_err}",
        )
