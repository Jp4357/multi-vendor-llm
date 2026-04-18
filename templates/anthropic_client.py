"""
Anthropic client — text only.
Requires: pip install anthropic python-dotenv
Env var:  ANTHROPIC_API_KEY (loaded from .env automatically)
"""
import os
from typing import Generator
from dotenv import load_dotenv
import anthropic

load_dotenv()  # loads ANTHROPIC_API_KEY from .env file

_client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 1024


# ── Single-shot ───────────────────────────────────────────────────────────────

def chat(prompt: str, model: str = DEFAULT_MODEL, system: str = None, max_tokens: int = DEFAULT_MAX_TOKENS, **kwargs) -> str:
    """Send a single prompt and return the full reply as a string."""
    kwargs_final = {"max_tokens": max_tokens, **kwargs}
    if system:
        kwargs_final["system"] = system
    message = _client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **kwargs_final
    )
    return message.content[0].text


def stream_chat(prompt: str, model: str = DEFAULT_MODEL, system: str = None, max_tokens: int = DEFAULT_MAX_TOKENS, **kwargs) -> Generator[str, None, None]:
    """Stream a single prompt. Yields text chunks as they arrive."""
    kwargs_final = {"max_tokens": max_tokens, **kwargs}
    if system:
        kwargs_final["system"] = system
    with _client.messages.stream(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **kwargs_final
    ) as stream:
        yield from stream.text_stream


# ── Multi-turn session ────────────────────────────────────────────────────────

class ChatSession:
    """Stateful multi-turn conversation. Maintains full message history."""

    def __init__(self, model: str = DEFAULT_MODEL, system: str = None, max_tokens: int = DEFAULT_MAX_TOKENS):
        self.model = model
        self.max_tokens = max_tokens
        self._system = system
        self._history: list[dict] = []

    @property
    def history(self) -> list[dict]:
        return self._history

    def reset(self):
        """Clear conversation history."""
        self._history = []

    def chat(self, prompt: str, **kwargs) -> str:
        """Send a message and return the full reply. History is updated automatically."""
        self._history.append({"role": "user", "content": prompt})
        kwargs_final = {"max_tokens": self.max_tokens, **kwargs}
        if self._system:
            kwargs_final["system"] = self._system
        message = _client.messages.create(model=self.model, messages=self._history, **kwargs_final)
        reply = message.content[0].text
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def stream_chat(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Stream a message. Yields chunks; history is updated when stream completes."""
        self._history.append({"role": "user", "content": prompt})
        kwargs_final = {"max_tokens": self.max_tokens, **kwargs}
        if self._system:
            kwargs_final["system"] = self._system
        full_reply = []
        with _client.messages.stream(model=self.model, messages=self._history, **kwargs_final) as stream:
            for text in stream.text_stream:
                full_reply.append(text)
                yield text
        self._history.append({"role": "assistant", "content": "".join(full_reply)})


# ── Unsupported modalities ────────────────────────────────────────────────────

def generate_image(prompt: str, **kwargs) -> list:
    raise NotImplementedError("Anthropic does not support image generation.")


def text_to_speech(text: str, **kwargs) -> bytes:
    raise NotImplementedError("Anthropic does not support TTS.")


def transcribe(audio_path: str, **kwargs) -> str:
    raise NotImplementedError("Anthropic does not support STT/transcription.")


# ── Environment check ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key or key == "your-api-key-here":
        print("ERROR: ANTHROPIC_API_KEY is not set. Add it to your .env file.")
    else:
        print("OK: ANTHROPIC_API_KEY is set.")
        print("Run your code to make your first API call.")
