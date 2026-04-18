"""
Ollama client — local or cloud inference.
Requires: pip install ollama python-dotenv

Local mode:  Ollama installed and running (https://ollama.com/download), no API key needed.
Cloud mode:  Set OLLAMA_API_KEY in .env to use Ollama's hosted cloud API.
"""
import os
import sys
from typing import Generator
from dotenv import load_dotenv
from ollama import Client

load_dotenv()  # loads OLLAMA_API_KEY from .env if present

_api_key = os.environ.get("OLLAMA_API_KEY")

# Use cloud client if API key is set, otherwise fall back to local
if _api_key:
    _client = Client(
        host="https://ollama.com",
        headers={"Authorization": f"Bearer {_api_key}"},
    )
    _mode = "cloud"
else:
    _client = Client()  # connects to local Ollama (http://localhost:11434)
    _mode = "local"

# ── FEATURE:chat ──────────────────────────────────────────────────────────────
DEFAULT_MODEL = "llama3.2"
# ── END FEATURE:chat ──────────────────────────────────────────────────────────


# ── FEATURE:chat ──────────────────────────────────────────────────────────────

def chat(prompt: str, model: str = DEFAULT_MODEL, system: str = None, **kwargs) -> str:
    """Send a single prompt and return the full reply."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = _client.chat(model=model, messages=messages, **kwargs)
    return response.message.content


def stream_chat(prompt: str, model: str = DEFAULT_MODEL, system: str = None, **kwargs) -> Generator[str, None, None]:
    """Stream a single prompt. Yields text chunks as they arrive."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    stream = _client.chat(model=model, messages=messages, stream=True, **kwargs)
    for chunk in stream:
        delta = chunk.message.content
        if delta:
            yield delta


class ChatSession:
    """Stateful multi-turn conversation. Maintains full message history."""

    def __init__(self, model: str = DEFAULT_MODEL, system: str = None):
        self.model = model
        self._history: list[dict] = []
        if system:
            self._history.append({"role": "system", "content": system})

    @property
    def history(self) -> list[dict]:
        return self._history

    def reset(self):
        """Clear conversation history (keeps system prompt if set)."""
        self._history = [m for m in self._history if m["role"] == "system"]

    def chat(self, prompt: str, **kwargs) -> str:
        """Send a message and return the full reply. History is updated automatically."""
        self._history.append({"role": "user", "content": prompt})
        response = _client.chat(model=self.model, messages=self._history, **kwargs)
        reply = response.message.content
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def stream_chat(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Stream a message. Yields chunks; history is updated when stream completes."""
        self._history.append({"role": "user", "content": prompt})
        stream = _client.chat(model=self.model, messages=self._history, stream=True, **kwargs)
        full_reply = []
        for chunk in stream:
            delta = chunk.message.content
            if delta:
                full_reply.append(delta)
                yield delta
        self._history.append({"role": "assistant", "content": "".join(full_reply)})

# ── END FEATURE:chat ──────────────────────────────────────────────────────────


# ── Environment check ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Mode: {_mode}")
    if _mode == "cloud":
        print("OK: OLLAMA_API_KEY is set — using Ollama cloud API.")
    else:
        print("No OLLAMA_API_KEY found — using local Ollama (http://localhost:11434).")
        print(f"Make sure Ollama is running and '{DEFAULT_MODEL}' is pulled:")
        print(f"  ollama serve")
        print(f"  ollama pull {DEFAULT_MODEL}")
