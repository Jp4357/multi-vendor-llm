"""
OpenAI client — text, image generation, TTS, STT.
Requires: pip install openai python-dotenv
Env var:  OPENAI_API_KEY (loaded from .env automatically)
"""
import os
from typing import Generator
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # loads OPENAI_API_KEY from .env file

_client = OpenAI()  # reads OPENAI_API_KEY from environment

# ── FEATURE:chat ──────────────────────────────────────────────────────────────
DEFAULT_CHAT_MODEL = "gpt-4o"
# ── END FEATURE:chat ──────────────────────────────────────────────────────────

# ── FEATURE:image ─────────────────────────────────────────────────────────────
DEFAULT_IMAGE_MODEL = "gpt-image-1.5"
# ── END FEATURE:image ─────────────────────────────────────────────────────────

# ── FEATURE:tts ───────────────────────────────────────────────────────────────
DEFAULT_TTS_MODEL = "tts-1"
DEFAULT_TTS_VOICE = "alloy"
# ── END FEATURE:tts ───────────────────────────────────────────────────────────

# ── FEATURE:stt ───────────────────────────────────────────────────────────────
DEFAULT_STT_MODEL = "whisper-1"
# ── END FEATURE:stt ───────────────────────────────────────────────────────────


# ── FEATURE:chat ──────────────────────────────────────────────────────────────

def chat(prompt: str, model: str = DEFAULT_CHAT_MODEL, system: str = None, **kwargs) -> str:
    """Send a single prompt and return the full reply as a string."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = _client.chat.completions.create(model=model, messages=messages, **kwargs)
    return response.choices[0].message.content


def stream_chat(prompt: str, model: str = DEFAULT_CHAT_MODEL, system: str = None, **kwargs) -> Generator[str, None, None]:
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

    def __init__(self, model: str = DEFAULT_CHAT_MODEL, system: str = None):
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


# ── FEATURE:image ─────────────────────────────────────────────────────────────

def generate_image(prompt: str, model: str = DEFAULT_IMAGE_MODEL, size: str = "1024x1024", n: int = 1) -> list[str]:
    """Generate image(s) and return a list of URLs."""
    response = _client.images.generate(model=model, prompt=prompt, size=size, n=n)
    return [item.url for item in response.data]

# ── END FEATURE:image ─────────────────────────────────────────────────────────


# ── FEATURE:tts ───────────────────────────────────────────────────────────────

def text_to_speech(text: str, output_path: str = "output.mp3", model: str = DEFAULT_TTS_MODEL, voice: str = DEFAULT_TTS_VOICE) -> str:
    """Convert text to speech, save to file, return the output path."""
    response = _client.audio.speech.create(model=model, voice=voice, input=text)
    response.stream_to_file(output_path)
    return output_path

# ── END FEATURE:tts ───────────────────────────────────────────────────────────


# ── FEATURE:stt ───────────────────────────────────────────────────────────────

def transcribe(audio_path: str, model: str = DEFAULT_STT_MODEL, language: str = None) -> str:
    """Transcribe an audio file to text using Whisper."""
    kwargs = {"language": language} if language else {}
    with open(audio_path, "rb") as f:
        transcript = _client.audio.transcriptions.create(model=model, file=f, **kwargs)
    return transcript.text

# ── END FEATURE:stt ───────────────────────────────────────────────────────────


# ── Environment check ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("OPENAI_API_KEY")
    if not key or key == "your-api-key-here":
        print("ERROR: OPENAI_API_KEY is not set. Add it to your .env file.")
    else:
        print("OK: OPENAI_API_KEY is set.")
        print("Run your code to make your first API call.")
