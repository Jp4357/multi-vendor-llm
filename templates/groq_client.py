"""
Groq client — ultra-fast text inference via LPU hardware.
Requires: pip install groq python-dotenv
Env var:  GROQ_API_KEY (loaded from .env automatically)
API is OpenAI-compatible.
"""
import os
from typing import Generator
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # loads GROQ_API_KEY from .env file

_client = Groq()  # reads GROQ_API_KEY from environment

# ── FEATURE:chat ──────────────────────────────────────────────────────────────
DEFAULT_MODEL = "llama-3.3-70b-versatile"
# ── END FEATURE:chat ──────────────────────────────────────────────────────────


# ── FEATURE:chat ──────────────────────────────────────────────────────────────

def chat(prompt: str, model: str = DEFAULT_MODEL, system: str = None, **kwargs) -> str:
    """Send a single prompt and return the full reply as a string."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = _client.chat.completions.create(model=model, messages=messages, **kwargs)
    return response.choices[0].message.content


def stream_chat(prompt: str, model: str = DEFAULT_MODEL, system: str = None, **kwargs) -> Generator[str, None, None]:
    """Stream a single prompt. Yields text chunks as they arrive."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    stream = _client.chat.completions.create(model=model, messages=messages, stream=True, **kwargs)
    for chunk in stream:
        delta = chunk.choices[0].delta.content
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
        response = _client.chat.completions.create(model=self.model, messages=self._history, **kwargs)
        reply = response.choices[0].message.content
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def stream_chat(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Stream a message. Yields chunks; history is updated when stream completes."""
        self._history.append({"role": "user", "content": prompt})
        stream = _client.chat.completions.create(model=self.model, messages=self._history, stream=True, **kwargs)
        full_reply = []
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_reply.append(delta)
                yield delta
        self._history.append({"role": "assistant", "content": "".join(full_reply)})

# ── END FEATURE:chat ──────────────────────────────────────────────────────────


# ── Environment check ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("GROQ_API_KEY")
    if not key or key == "your-api-key-here":
        print("ERROR: GROQ_API_KEY is not set. Add it to your .env file.")
    else:
        print("OK: GROQ_API_KEY is set.")
        print("Run your code to make your first API call.")
