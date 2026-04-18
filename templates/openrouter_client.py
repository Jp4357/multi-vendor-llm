"""
OpenRouter client — unified gateway to 300+ models.
Requires: pip install openai python-dotenv  (uses OpenAI SDK with a base_url swap)
Env var:  OPENROUTER_API_KEY (loaded from .env automatically)
Full model list: https://openrouter.ai/models
"""
import os
from typing import Generator
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # loads OPENROUTER_API_KEY from .env file

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY", ""),
)

# Any OpenRouter model ID works — examples:
#   "openai/gpt-4.1"                  OpenAI
#   "anthropic/claude-sonnet-4-6"     Anthropic
#   "google/gemini-2.5-flash"         Google (default)
#   "meta-llama/llama-4-scout"        Meta
#   "mistralai/mistral-large"         Mistral
DEFAULT_MODEL = "google/gemini-2.5-flash"


# ── Single-shot ───────────────────────────────────────────────────────────────

def chat(prompt: str, model: str = DEFAULT_MODEL, system: str = None, **kwargs) -> str:
    """Send a single prompt through OpenRouter and return the full reply."""
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


# ── Multi-turn session ────────────────────────────────────────────────────────

class ChatSession:
    """Stateful multi-turn conversation. Switch models per-session."""

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


# ── Unsupported modalities ────────────────────────────────────────────────────

def generate_image(prompt: str, **kwargs) -> list:
    raise NotImplementedError(
        "OpenRouter chat completions do not support image generation. "
        "Use openai_client.py (DALL-E) or gemini_client.py (Imagen) instead."
    )


def text_to_speech(text: str, **kwargs) -> bytes:
    raise NotImplementedError("OpenRouter does not expose TTS endpoints.")


def transcribe(audio_path: str, **kwargs) -> str:
    raise NotImplementedError("OpenRouter does not expose STT/transcription endpoints.")


# ── Environment check ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key or key == "your-api-key-here":
        print("ERROR: OPENROUTER_API_KEY is not set. Add it to your .env file.")
    else:
        print("OK: OPENROUTER_API_KEY is set.")
        print("Run your code to make your first API call.")
